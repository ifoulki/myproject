-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 10, 2025 at 07:53 PM
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
-- Table structure for table `synonym_terms`
--

CREATE TABLE `synonym_terms` (
  `id` int(11) NOT NULL,
  `term` varchar(255) NOT NULL,
  `synonyms` longtext NOT NULL,
  `ignore_terms` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `synonym_terms`
--

INSERT INTO `synonym_terms` (`id`, `term`, `synonyms`, `ignore_terms`) VALUES
(9, 'إبن', 'ولد، فلذة الكبد', 'ثيضصبضصث'),
(11, 'خال', ' أخ الأم، أخ الخال، إبن الجد', 'خالد،\r\nمركز الاتصال،\r\nمركز اتصال'),
(12, 'أم', 'والدة، مامات', 'ثيضصبضصث'),
(13, 'أخت', 'شقيقة، خت ', 'بصثق'),
(14, 'خالة', 'أخت الأم، شقيقة الأم', 'ثيضصبضصث'),
(15, 'عمة', 'أخت الأب، شقيقة الأب', 'ثيضصبضصث'),
(16, 'جد', 'والد الأب، والد الأم', 'ثيضصبضصث'),
(17, 'زوجة', 'شريكة الحياة، مراة', 'ثيضصبضصث'),
(18, 'حماة', 'والدة الزوجة، والدة الزوج', 'ثيضصبضصث'),
(20, 'عمتي', 'أخت أبي،أخت عمي', 'ثيضصبضصث'),
(21, 'زينة', 'زينة', 'الخزينة');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `synonym_terms`
--
ALTER TABLE `synonym_terms`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `synonym_terms`
--
ALTER TABLE `synonym_terms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
