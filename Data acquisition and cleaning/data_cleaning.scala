package sparkcoredemo.sparksqldemo.main

import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.types.{DoubleType, IntegerType, StringType, StructField, StructType}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}

object data_cleaning {
  def main(args: Array[String]): Unit = {
    val sc: SparkConf = new SparkConf().setMaster("local[*]").setAppName("data_cleaning")
    val spark: SparkSession = SparkSession.builder().config(sc).getOrCreate()

    //从MySQL数据库中加载数据生成DataFrame：original_DF
    val original_DF: DataFrame = spark.read
      .format("jdbc")
      .option("driver", "com.mysql.cj.jdbc.Driver")
      .option("url", "jdbc:mysql://localhost:3306/pydb")
      .option("dbtable", "house")
      .option("user", "root")
      .option("password", "123456")
      .load()

    //将DataFrame转为由 Row 对象组成的 RDD：original_RDD
    val original_RDD: RDD[Row] = original_DF.rdd

    // map()分别从每个 Row 对象中执行提取出相应的字段的函数，将其转换为一个元组。
    // 最终转为包含多个元组的多维数组：original_Array
    val original_Array: Array[(String, String, String, String, String, String, String, Int, String, String)] = original_RDD.map((row: Row) =>
      (row.getString(0), row.getString(1), row.getString(2), row.getString(3), row.getString(4),
        row.getString(5), row.getString(6), row.getInt(7), row.getString(8), row.getString(9))  //每一行中，并将它们放入元组中。
    ).collect()

    //定义数据清洗方法：data_Cleaning()，接受一个元组作为参数，最后返回一个新的元组，即清洗后的字段。
    def data_Cleaning(tuple: (String, String, String, String, String, String, String, Int, String, String)):
    (String, String, String, String, Double, String, String, Int, String, String) = {
      // 使用正则表达式替换掉房源简介中的所有空格符
      val newA: String = tuple._1.replaceAll("\\s", "")
      // 提取房源户型，按空格分割后取第一部分，因为后两部分不需要
      val newD: String = tuple._4.split(" ")(0)
      // 使用正则表达式替换掉 所有非数字和小数点字符，即"面积：" 和“平方米”部分，并转为Double类型数据
      val newE: Double = tuple._5.replaceAll("[^\\d.]+", "").toDouble
      // 使用正则表达式替换掉 "楼层：" 部分
      val newF: String = tuple._6.replace("楼层：", "")
      // 使用正则表达式替换掉 "朝向：" 部分
      val newG: String = tuple._7.replace("朝向：", "")
      // 使用正则表达式替换掉 "采暖：" 部分
      val newI: String = tuple._9.replace("采暖：", "")
      // 返回新的元组
      return (newA, tuple._2, tuple._3, newD, newE, newF, newG, tuple._8, newI, tuple._10)
    }

    //获取清洗后的数组：new_Array,将 data_Cleaning 清洗函数应用于 original_Array 中的每个元素
    val new_Array: Array[(
      String, String, String, String, Double, String, String, Int, String, String)] =
      original_Array.map(data_Cleaning)

  //定义 DataFrame 的模式信息
  val schema: StructType = StructType(Seq(
    StructField("house_Introduce", StringType, nullable = true),
    StructField("house_Region", StringType, nullable = true),
    StructField("house_Address", StringType, nullable = true),
    StructField("house_Type", StringType, nullable = true),
    StructField("house_Area", DoubleType, nullable = true),
    StructField("house_floor", StringType, nullable = true),
    StructField("house_Direction", StringType, nullable = true),
    StructField("house_Price", IntegerType, nullable = true),
    StructField("house_Heating", StringType, nullable = true),
    StructField("house_Lease", StringType, nullable = true)
  ))

  // 将数组转换为 RDD[Row]：newRDD，parallelize ()将数组转换为 RDD,将每个元组转换为 Row 对象
    val newRDD: RDD[Row] = spark.sparkContext.parallelize(new_Array).map {
      case (house_Introduce, house_Region, house_Address, house_Type, house_Area, house_floor, house_Direction, house_Price, house_Heating, house_Lease
        ) =>
        Row(house_Introduce, house_Region, house_Address, house_Type, house_Area, house_floor, house_Direction, house_Price, house_Heating, house_Lease)
    }

    // 创建新的DataFrame，将模式和数据对应拼接
    val new_DF: DataFrame = spark.createDataFrame(newRDD, schema)

//    new_DF.show()
    new_DF.write
      .format("jdbc")
      .option("driver", "com.mysql.cj.jdbc.Driver")
      .option("url", "jdbc:mysql://localhost:3306/pydb")
      .option("dbtable", "house_data_cleaning")
      .option("user", "root")
      .option("password", "123456")
      .mode("append")
      .save()
  }
}
