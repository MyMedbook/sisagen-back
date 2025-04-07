from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from api.models.report import Report
from api.models import *
from api.serializers.report import ReportSerializer, QuickReportSerializer
from api.views.base import ReportPagination
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class VerificationView(APIView):

    def get_latest(self, pk, model):
        latest: BaseDocument = model.objects(paziente_id=pk).order_by('-created_at').first()
        if not latest:
            return False
        target_date = datetime.now() - timedelta(days=180)
        return latest.created_at > target_date

    def get(self, request, paziente_id):

        tabs = {
            "fattori-rischio": FattoriRischio,
            "comorbidita": Comorbidita,
            "sintomatologia": Sintomatologia,
            "coinvolgimento": CoinvolgimentoMultisistemico,
            "terapia": TerapiaFarmacologica,
            "ecg": ECG,
            "ecocardiogramma": Ecocardiogramma,
            "esami_laboratorio": EsamiLaboratorio,
            "genetica": Genetica,
            "pedigree": Pedigree
        }
        verification = {tab: self.get_latest(paziente_id, model) for tab, model in tabs.items()}
        return Response(verification)


class ReportView(APIView):
    """
    View for handling patient reports
    """
    pagination_class = ReportPagination

    def get_paginated_response(self, data, serializer_class):
        """Helper method to get paginated response"""
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, self.request)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = serializer_class(data, many=True)
        return Response(serializer.data)

    def get(self, request, paziente_id, report_id=None):
        """Get report(s) for a patient"""
        try:
            if report_id:
                # Get specific report
                report = Report.objects(paziente_id=paziente_id, report_id=report_id).first()
                if not report:
                    raise NotFound(f"Report {report_id} not found for patient {paziente_id}")
                
                serializer = ReportSerializer(report)
                return Response(serializer.data)
            else:
                # Get all reports with pagination
                reports = Report.objects(paziente_id=paziente_id).order_by('-report_id')
                return self.get_paginated_response(reports, ReportSerializer)

        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in Report GET: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, paziente_id):
        """Create a new report"""
        try:
            # Create new report instance
            report = Report(
                paziente_id=paziente_id,
                operatore_id=request.data.get('operatore_id'),
                paziente_nome=request.data.get('paziente_nome'),
                paziente_cognome=request.data.get('paziente_cognome'),
                operatore_nome=request.data.get('operatore_nome'),
                operatore_cognome=request.data.get('operatore_cognome'),
                structure=request.data.get('structure'),
                report_id=Report.get_next_report_id(paziente_id)
            )

            # Get latest records for all sections
            latest_records = report.get_latest_records()

            # Validate that we have at least one record
            if not any(latest_records.values()):
                raise ValidationError("No records found for this patient")

            # Assign references to the report
            for field, record in latest_records.items():
                if record:
                    setattr(report, field, record)

            # Save the report
            report.save()

            # Return the serialized report
            serializer = ReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in Report POST: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, paziente_id, report_id):
        """Delete a specific report"""
        try:
            report = Report.objects(paziente_id=paziente_id, report_id=report_id).first()
            if not report:
                raise NotFound(f"Report {report_id} not found for patient {paziente_id}")

            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in Report DELETE: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class QuickReportView(APIView):
    """
    View for handling quick report metadata
    """
    pagination_class = ReportPagination

    def get(self, request, paziente_id):
        """Get all reports metadata for a patient"""
        try:
            reports = Report.objects(paziente_id=paziente_id).order_by('-report_id')
            
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(reports, request)
            
            if page is not None:
                serializer = QuickReportSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = QuickReportSerializer(reports, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error in QuickReport GET: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class QuickReportAllView(APIView):
    """
    View for handling all patients' quick report metadata
    """
    pagination_class = ReportPagination

    def get(self, request):
        """Get all reports metadata grouped by patient"""
        try:
            # Get all reports ordered by patient_id and report_id
            reports = Report.objects.order_by('paziente_id', '-report_id')
            
            # Group reports by patient_id
            grouped_reports = defaultdict(list)
            for report in reports:
                report_data = {
                    'report_id': report.report_id,
                    'paziente_id': report.paziente_id,
                    'paziente_nome': report.paziente_nome,
                    'paziente_cognome': report.paziente_cognome,
                    'operatore_id': report.operatore_id,
                    'operatore_nome': report.operatore_nome,
                    'operatore_cognome': report.operatore_cognome,
                    'status': report.status,
                    'created_at': report.created_at,
                    'updated_at': report.updated_at
                }
                grouped_reports[report.paziente_id].append(report_data)
            
            # Convert to list format for pagination
            result = [
                {
                    'paziente_id': paziente_id,
                    'paziente_nome': reports_list[0]['paziente_nome'],
                    'paziente_cognome': reports_list[0]['paziente_cognome'],
                    'reports': reports_list
                }
                for paziente_id, reports_list in grouped_reports.items()
            ]
            
            # Apply pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(result, request)
            
            if page is not None:
                return paginator.get_paginated_response(page)
            
            return Response(result)

        except Exception as e:
            logger.error(f"Error in QuickReportAll GET: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )