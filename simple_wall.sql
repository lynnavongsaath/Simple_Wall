-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: localhost    Database: simple_wall
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `messager_id` int(11) NOT NULL,
  `messagee_id` int(11) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_messages_users_idx` (`messager_id`),
  KEY `fk_messages_users1_idx` (`messagee_id`),
  CONSTRAINT `fk_messages_users` FOREIGN KEY (`messager_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_messages_users1` FOREIGN KEY (`messagee_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (5,5,7,'Hi there Aretha!','2018-10-16 13:46:47','2018-10-16 13:46:47'),(6,5,7,'can you help me on an assignment?','2018-10-16 13:48:51','2018-10-16 13:48:51'),(7,5,7,'Thanks Aretha for all your help!','2018-10-16 13:48:53','2018-10-16 13:48:53'),(22,7,5,'Hi Star!','2018-10-17 11:25:00','2018-10-17 11:25:00'),(23,5,6,'HI John','2018-10-17 11:30:53','2018-10-17 11:30:53');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (5,'Star','Vongsaath','star.vongsaath@gmail.com','$2b$12$2eU80nhGDEBOptYwIB4.YeRQZqruOmq.UfJiAwLeBg1qNhdJzk/T6','2018-10-16 13:32:49','2018-10-16 13:32:49'),(6,'John','Smith','john.smith@gmail.com','$2b$12$yBFWiNY9lFU/BjjKayqzJeFDLuLVgAmmmDJQ9XxgAvx3vStX.i9mK','2018-10-16 13:42:34','2018-10-16 13:42:34'),(7,'Aretha','Franklin','aretha.franklin@gmail.com','$2b$12$zZqd8TXcyXOefJ5bYnlrU.IZK/Kx/1Wx3Uh7ZZVH71AGjXH.CaZzW','2018-10-16 13:43:12','2018-10-16 13:43:12'),(8,'Billy','Jean','billy.jean@gmail.com','$2b$12$srNH.fwu10nhxzD5x0Tuju.FQr9tZ8uugmvA51gCdZiPWUo9Y0wvO','2018-10-17 11:32:13','2018-10-17 11:32:13');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-17 11:39:34
