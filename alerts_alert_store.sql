-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: alerts
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alert_store`
--

DROP TABLE IF EXISTS `alert_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alert_store` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_notify` date DEFAULT NULL,
  `time_notify` time DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `time_created` time DEFAULT NULL,
  `userID` varchar(256) DEFAULT NULL,
  `delta` varchar(256) DEFAULT NULL,
  `note` varchar(256) DEFAULT NULL,
  `sent` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert_store`
--

LOCK TABLES `alert_store` WRITE;
/*!40000 ALTER TABLE `alert_store` DISABLE KEYS */;
INSERT INTO `alert_store` VALUES (16,'2021-05-14','17:40:00','2021-05-14','17:11:40','135080434773131264','0:28:19.869301','mememem',1),(17,'2021-05-14','17:19:00','2021-05-14','17:17:12','135080434773131264','0:01:48.159923','LETS GOOOOO',1),(18,'2021-05-14','17:32:00','2021-05-14','17:31:33','135080434773131264','0:00:27.154392','LETS GOOOOO',1),(19,'2021-05-14','17:36:00','2021-05-14','17:35:10','135080434773131264','0:00:49.867163','LET\'S GOOOOO',1),(20,'2021-05-14','17:37:00','2021-05-14','17:36:28','135080434773131264','0:00:32.305256','lemon gang rise up ?',1),(21,'2021-05-14','17:38:00','2021-05-14','17:37:56','135080434773131264','0:00:04.313735','??? A M O G U S ???',1),(22,'2021-05-14','17:42:00','2021-05-14','17:41:24','134670639784132608','0:00:36.284331','Hi',1),(23,'2021-05-14','17:43:00','2021-05-14','17:42:15','135080434773131264','0:00:44.643330','<@!134670639784132608>',1),(24,'2021-05-14','17:47:00','2021-05-14','17:46:25','135080434773131264','0:00:34.932945','doiasdhsai0odas',1);
/*!40000 ALTER TABLE `alert_store` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-14 18:14:57
