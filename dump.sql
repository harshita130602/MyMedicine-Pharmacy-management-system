
-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: localhost    Database: MYMEDICINE
-- ------------------------------------------------------
-- Server version	8.0.21-0ubuntu0.20.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CART`
--

DROP TABLE IF EXISTS `CART`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CART` (
  `Cart_id` varchar(10) NOT NULL,
  `Items` int DEFAULT NULL,
  `Cart_total_price` float NOT NULL,
  PRIMARY KEY (`Cart_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CART`
--

LOCK TABLES `CART` WRITE;
/*!40000 ALTER TABLE `CART` DISABLE KEYS */;
INSERT INTO `CART` VALUES ('C1',0,0);
/*!40000 ALTER TABLE `CART` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CART_ITEM`
--

DROP TABLE IF EXISTS `CART_ITEM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CART_ITEM` (
  `Cart_id` varchar(10) NOT NULL,
  `Medicine_id` varchar(10) NOT NULL,
  `Quantity` int NOT NULL,
  `Total_price` float NOT NULL,
  KEY `Medicine_id` (`Medicine_id`),
  CONSTRAINT `CART_ITEM_ibfk_1` FOREIGN KEY (`Medicine_id`) REFERENCES `MEDICINE` (`Medicine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CART_ITEM`
--

LOCK TABLES `CART_ITEM` WRITE;
/*!40000 ALTER TABLE `CART_ITEM` DISABLE KEYS */;
/*!40000 ALTER TABLE `CART_ITEM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CUSTOMER`
--

DROP TABLE IF EXISTS `CUSTOMER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CUSTOMER` (
  `User_id` varchar(10) NOT NULL,
  `Cart_id` varchar(10) NOT NULL,
  PRIMARY KEY (`User_id`),
  CONSTRAINT `CUSTOMER_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `USER` (`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CUSTOMER`
--

LOCK TABLES `CUSTOMER` WRITE;
/*!40000 ALTER TABLE `CUSTOMER` DISABLE KEYS */;
INSERT INTO `CUSTOMER` VALUES ('CU1','C1');
/*!40000 ALTER TABLE `CUSTOMER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EMPLOYEE`
--

DROP TABLE IF EXISTS `EMPLOYEE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EMPLOYEE` (
  `User_id` varchar(10) NOT NULL,
  `Role` varchar(10) NOT NULL,
  `Items_updated` int DEFAULT NULL,
  `Orders_updated` int DEFAULT NULL,
  `Supervisor_id` varchar(10) DEFAULT NULL,
  `Working` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`User_id`),
  CONSTRAINT `EMPLOYEE_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `USER` (`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPLOYEE`
--

LOCK TABLES `EMPLOYEE` WRITE;
/*!40000 ALTER TABLE `EMPLOYEE` DISABLE KEYS */;
INSERT INTO `EMPLOYEE` VALUES ('AD1','Admin',NULL,NULL,'',1),('AD2','Manager',NULL,NULL,'AD1',1),('AD3','Manager',NULL,NULL,'AD1',1),('AD4','Manager',NULL,NULL,'AD1',0);
/*!40000 ALTER TABLE `EMPLOYEE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEDICINE`
--

DROP TABLE IF EXISTS `MEDICINE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MEDICINE` (
  `Medicine_id` varchar(10) NOT NULL,
  `Medicine_name` varchar(40) NOT NULL,
  `Medicine_price` float NOT NULL,
  `Medicine_description` longtext,
  `Manufacturer` varchar(40) NOT NULL,
  `Added_at` datetime NOT NULL,
  `Added_by` varchar(10) NOT NULL,
  `Updated_at` datetime DEFAULT NULL,
  `Updated_by` varchar(10) DEFAULT NULL,
  `Medicine_stock` int DEFAULT '0',
  `Expiry_date` date NOT NULL,
  PRIMARY KEY (`Medicine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEDICINE`
--

LOCK TABLES `MEDICINE` WRITE;
/*!40000 ALTER TABLE `MEDICINE` DISABLE KEYS */;
INSERT INTO `MEDICINE` VALUES ('M1','Paracitamol',60,'Drug for Headache','Calpol','2020-10-04 23:41:37','AD1','2020-10-04 23:41:37','AD1',500,'2022-09-18'),('M10','Xanax',300,'Anxiety Disorder','Xanax','2020-10-04 23:49:18','AD1','2020-10-04 23:49:18','AD1',100,'2022-09-18'),('M11','Azithral',125,'Antibiotic','Azithral','2020-10-05 00:00:43','AD1','2020-10-05 00:08:59','AD2',1,'2022-09-18'),('M2','Acetaminophen',200,'Reduces fever','Ultracet','2020-10-04 23:43:14','AD1','2020-10-04 23:43:14','AD1',600,'2022-09-18'),('M3','Adderall',500,'CNS Simulant','Mydayis','2020-10-04 23:43:54','AD1','2020-10-04 23:43:54','AD1',93,'2022-09-18'),('M4','Benzonatate',250,'Non Narcotic Cough Medicine','Zonatuss','2020-10-04 23:44:51','AD1','2020-10-04 23:44:51','AD1',300,'2022-09-18'),('M5','Brilinta',390,'Removal of unwanted blood clot','Brilinta','2020-10-04 23:45:35','AD1','2020-10-04 23:45:35','AD1',400,'2022-09-18'),('M6','Cephalexin',750,'Antibiotic','Keflex','2020-10-04 23:46:06','AD1','2020-10-04 23:46:06','AD1',100,'2022-09-18'),('M7','Ciprofloxacin',75,'Antibiotic','Cipro','2020-10-04 23:46:39','AD1','2020-10-04 23:46:39','AD1',900,'2022-09-18'),('M8','Doxycycline',400,'Used to treat Bacterial Infections','Adoxa','2020-10-04 23:47:53','AD1','2020-10-04 23:47:53','AD1',200,'2022-09-18'),('M9','Dupixent',100,'Asthma','Dupixent','2020-10-04 23:48:42','AD1','2020-10-04 23:48:42','AD1',400,'2022-09-18');
/*!40000 ALTER TABLE `MEDICINE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MOBILE_NUMBER`
--

DROP TABLE IF EXISTS `MOBILE_NUMBER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MOBILE_NUMBER` (
  `User_id` varchar(10) NOT NULL,
  `Mobile_number` decimal(10,0) DEFAULT NULL,
  KEY `User_id` (`User_id`),
  CONSTRAINT `MOBILE_NUMBER_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `USER` (`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MOBILE_NUMBER`
--

LOCK TABLES `MOBILE_NUMBER` WRITE;
/*!40000 ALTER TABLE `MOBILE_NUMBER` DISABLE KEYS */;
/*!40000 ALTER TABLE `MOBILE_NUMBER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ORDER_ITEM`
--

DROP TABLE IF EXISTS `ORDER_ITEM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ORDER_ITEM` (
  `Order_id` varchar(40) NOT NULL,
  `Medicine_id` varchar(40) NOT NULL,
  `Quantity` int NOT NULL,
  `Total_price` float NOT NULL,
  KEY `Order_id` (`Order_id`),
  KEY `Medicine_id` (`Medicine_id`),
  CONSTRAINT `ORDER_ITEM_ibfk_2` FOREIGN KEY (`Medicine_id`) REFERENCES `MEDICINE` (`Medicine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ORDER_ITEM`
--

LOCK TABLES `ORDER_ITEM` WRITE;
/*!40000 ALTER TABLE `ORDER_ITEM` DISABLE KEYS */;
INSERT INTO `ORDER_ITEM` VALUES ('FEFD10','M3',7,3500);
/*!40000 ALTER TABLE `ORDER_ITEM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ORDER_REQUEST`
--

DROP TABLE IF EXISTS `ORDER_REQUEST`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ORDER_REQUEST` (
  `Order_id` varchar(10) NOT NULL,
  `Cart_id` varchar(10) NOT NULL,
  `Total_price` float NOT NULL,
  `Items` int NOT NULL,
  `Mobile_number` decimal(10,0) DEFAULT NULL,
  `Address_line_1` varchar(40) NOT NULL,
  `Address_line_2` varchar(40) DEFAULT NULL,
  `City` varchar(40) NOT NULL,
  `State` varchar(40) NOT NULL,
  `Country` varchar(40) NOT NULL,
  `Updated_at` datetime DEFAULT NULL,
  `Updated_by` varchar(40) DEFAULT NULL,
  `Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Order_id`),
  KEY `Cart_id` (`Cart_id`),
  CONSTRAINT `ORDER_REQUEST_ibfk_1` FOREIGN KEY (`Cart_id`) REFERENCES `CART` (`Cart_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ORDER_REQUEST`
--

LOCK TABLES `ORDER_REQUEST` WRITE;
/*!40000 ALTER TABLE `ORDER_REQUEST` DISABLE KEYS */;
INSERT INTO `ORDER_REQUEST` VALUES ('FEFD10','C1',3500,1,123456789,'221B','Boring Road','Patna','Bihar','India','2020-10-05 01:29:45',NULL,1);
/*!40000 ALTER TABLE `ORDER_REQUEST` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRANSACTION`
--

DROP TABLE IF EXISTS `TRANSACTION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TRANSACTION` (
  `Transaction_id` varchar(10) NOT NULL,
  `Order_id` varchar(10) NOT NULL,
  `Payment_mode` varchar(40) NOT NULL,
  `Completed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Transaction_id`),
  KEY `Order_id` (`Order_id`),
  CONSTRAINT `TRANSACTION_ibfk_1` FOREIGN KEY (`Order_id`) REFERENCES `ORDER_REQUEST` (`Order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TRANSACTION`
--

LOCK TABLES `TRANSACTION` WRITE;
/*!40000 ALTER TABLE `TRANSACTION` DISABLE KEYS */;
INSERT INTO `TRANSACTION` VALUES ('19BC1B','FEFD10','NetBanking',1);
/*!40000 ALTER TABLE `TRANSACTION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USER` (
  `User_id` varchar(10) NOT NULL,
  `First_name` varchar(40) NOT NULL,
  `Last_name` varchar(40) DEFAULT NULL,
  `Email_id` varchar(40) NOT NULL,
  `Password` varchar(255) NOT NULL,
  PRIMARY KEY (`User_id`),
  UNIQUE KEY `Email_id` (`Email_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES ('AD1','Prajneya','Admin','prajneya@admin.com','81dc9bdb52d04dc20036dbd8313ed055'),('AD2','Prajneya','Manager 1','prajneya1@manager.com','81dc9bdb52d04dc20036dbd8313ed055'),('AD3','Prajneya','Manager 2','prajneya2@manager.com','81dc9bdb52d04dc20036dbd8313ed055'),('AD4','Prajneya','Manager 3','prajneya3@manager.com','81dc9bdb52d04dc20036dbd8313ed055'),('CU1','Prajneya','Customer','prajneya@customer.com','81dc9bdb52d04dc20036dbd8313ed055');
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-05 13:48:37