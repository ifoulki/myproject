-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 10, 2025 at 07:52 PM
-- Server version: 11.8.3-MariaDB-log
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `u980306597_tifinar`
--

-- --------------------------------------------------------

--
-- Table structure for table `results`
--

CREATE TABLE `results` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `exam_title` varchar(255) DEFAULT NULL,
  `exam_link` longtext DEFAULT NULL,
  `result` double DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `results`
--

INSERT INTO `results` (`id`, `name`, `exam_title`, `exam_link`, `result`, `created_at`, `updated_at`) VALUES
(1, 'dfqfsf', 'اختبار رقم 1 : الكمياء', 'https://tifinar.net/%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1_%D8%B1%D9%82%D9%85_1_:_%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1', 1.5, '2025-01-01 12:29:35', '2025-01-01 12:29:35'),
(6, 'أستاذ متدرب', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 19, '2025-07-12 10:53:41', '2025-07-12 10:53:41'),
(7, 'أستاذ متدرب', 'اختبار رقم 1 : الكمياء', 'https://tifinar.net/%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1_%D8%B1%D9%82%D9%85_1_%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1', 15, '2025-07-12 11:00:19', '2025-07-12 11:00:19'),
(8, 'موقع تيفيناغ', 'اختبار السياقة', 'https://tifinar.net/%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1_%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D9%82%D8%A9', 26, '2025-08-12 15:28:41', '2025-08-12 15:28:41'),
(9, 'موقع تيفيناغ', 'اختبار رقم 1 : الكمياء', 'https://tifinar.net/%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1_%D8%B1%D9%82%D9%85_1_%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1', 10, '2025-08-12 18:17:18', '2025-08-12 18:17:18'),
(10, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 7, '2025-08-12 18:40:04', '2025-08-12 18:40:04'),
(11, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 7, '2025-08-12 18:41:15', '2025-08-12 18:41:15'),
(12, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 8, '2025-08-12 18:41:30', '2025-08-12 18:41:30'),
(13, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 9, '2025-08-12 18:41:43', '2025-08-12 18:41:43'),
(14, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 10, '2025-08-12 18:41:58', '2025-08-12 18:41:58'),
(15, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 10, '2025-08-12 18:42:16', '2025-08-12 18:42:16'),
(16, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 11, '2025-08-12 18:42:35', '2025-08-12 18:42:35'),
(17, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 12, '2025-08-12 18:42:51', '2025-08-12 18:42:51'),
(18, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 3, '2025-08-12 18:43:27', '2025-08-12 18:43:27'),
(19, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 4, '2025-08-12 18:43:36', '2025-08-12 18:43:36'),
(20, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 6, '2025-08-12 18:44:03', '2025-08-12 18:44:03'),
(21, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 9, '2025-08-12 18:44:33', '2025-08-12 18:44:33'),
(22, 'موقع تيفيناغ', 'نموذج 1 : الفرض الأول في الفزياء والكمياء الدورة الأولى', 'https://tifinar.net/%D9%86%D9%85%D9%88%D8%B0%D8%AC_1_%D8%A7%D9%84%D9%81%D8%B1%D8%B6_%D8%A7%D9%84%D8%A3%D9%88%D9%84_%D9%81%D9%8A_%D8%A7%D9%84%D9%81%D8%B2%D9%8A%D8%A7%D8%A1_%D9%88%D8%A7%D9%84%D9%83%D9%85%D9%8A%D8%A7%D8%A1_%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D8%A9_%D8%A7%D9%84%D8%A3%D9%88%D9%84%D9%89', 13, '2025-08-12 18:45:08', '2025-08-12 18:45:08');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `results`
--
ALTER TABLE `results`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `results`
--
ALTER TABLE `results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
