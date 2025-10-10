-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 08, 2025 at 10:53 PM
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
-- Table structure for table `myadmin`
--

CREATE TABLE `myadmin` (
  `adm_id` tinyint(4) NOT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `mobile_logo` varchar(255) DEFAULT NULL,
  `link` longtext DEFAULT NULL,
  `ads` longtext DEFAULT NULL,
  `aside_ads` longtext DEFAULT NULL,
  `meta_title` varchar(255) DEFAULT NULL,
  `meta_description` text DEFAULT NULL,
  `meta_keyword` text DEFAULT '',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `myadmin`
--

INSERT INTO `myadmin` (`adm_id`, `logo`, `mobile_logo`, `link`, `ads`, `aside_ads`, `meta_title`, `meta_description`, `meta_keyword`, `created_at`, `updated_at`) VALUES
(1, 'logo.webp', 'Home.webp', '0', '<a target=\"_blank\" href=\"https://hostinger.ae?REFERRALCODE=1HAMID718\"><img src=\"assets/pub2.webp\"></a>', '<a target=\"_blank\" href=\"https://hostinger.ae?REFERRALCODE=1HAMID718\"><img src=\"../../assets/pub1.webp\"></a>', 'مجلة تيفيناغ', 'مجلة تيفيناغ هي مجلة متخصصة في نشر مواضيع ثقافية وتعليمية متوعة', '', '2024-12-06 23:00:00', '2024-12-06 23:00:00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `myadmin`
--
ALTER TABLE `myadmin`
  ADD PRIMARY KEY (`adm_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
