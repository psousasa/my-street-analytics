import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types


spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()


schema = types.StructType(
    [
        types.StructField("dt_registo", types.DateType(), True),
        types.StructField("area", types.StringType(), True),
        types.StructField("tipe", types.StringType(), True),
        types.StructField("Subseccao", types.IntegerType(), True),
        types.StructField("Freguesia", types.StringType(), True),
        types.StructField("Longitude_Subseccao", types.FloatType(), True),
        types.StructField("Latitude_Subseccao", types.FloatType(), True),
    ]
)


df = (
    spark.read.option("header", "true")
    .schema(schema)
    .csv(".csv.gz")
)
