from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from core.serializers import CsvSerializer
from rest_framework import status
import pandas as pd
from sqlalchemy import create_engine
from rest_framework import serializers
from sqlalchemy.sql import text
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class FileUploadView(APIView):
    """
    File Upload view saves the uploaded file
    and inserts the dataset into MySQL Database
    """

    serializer_class = CsvSerializer

    def put(self, request, *args, **kwargs) -> Response:

        serializer = CsvSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csv_file = serializer.validated_data["file"]
        if not csv_file.name.endswith(".csv"):
            raise serializers.ValidationError(
                "The file uploaded is not a csv file", code="invalid file"
            )
        serializer.save()
        table_name = csv_file.name.split(".")[0]
        engine = create_engine("mysql+pymysql://root:password@localhost/csv_store")
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, con=engine)

        return Response("Data set uploaded", status=status.HTTP_201_CREATED)


class DatasetDetailView(APIView):
    cols_params = openapi.Parameter('columns', openapi.IN_QUERY, description="Columns in Dataset", type=openapi.TYPE_STRING)
    conds_params = openapi.Parameter('conditions', openapi.IN_QUERY, description="Column Conditions", type=openapi.TYPE_STRING)
    @swagger_auto_schema(responses={200: {}}, manual_parameters=[cols_params, conds_params])
    def get(self, request, dataset_name) -> Response:
        columns = request.query_params.get("columns")
        conditions = request.query_params.get("conditions")
        engine = create_engine("mysql+pymysql://root:password@localhost/csv_store")
        if columns and conditions:            
            with engine.connect() as con:
                query = "SELECT {} FROM {} WHERE {} LIMIT 50;".format(
                    columns, dataset_name, conditions
                )
                statement = text(query)
                rows = con.execute(statement)
                return Response(rows, status=status.HTTP_200_OK)
        if columns:
            with engine.connect() as con:
                query = "SELECT {} FROM {} LIMIT 50;".format(columns, dataset_name)
                statement = text(query)
                rows = con.execute(statement)
                return Response(rows, status=status.HTTP_200_OK)
        if conditions:
            print(conditions)
            with engine.connect() as con:
                query = "SELECT * FROM {} WHERE {} LIMIT 50;".format(
                    dataset_name, conditions
                )
                statement = text(query)
                rows = con.execute(statement)
                return Response(rows, status=status.HTTP_200_OK)
        
        
        with engine.connect() as con:
            statement = text("SELECT * FROM {} LIMIT 50;".format(dataset_name))
            rows = con.execute(statement)

            con.close()
            return Response(
                rows,
                # [dict(zip(columns, row)) for row in cursor.fetchall()],
                status=status.HTTP_200_OK,
            )


