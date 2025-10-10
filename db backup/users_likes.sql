-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 10, 2025 at 07:54 PM
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
-- Table structure for table `users_likes`
--

CREATE TABLE `users_likes` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `ip_or_name` varchar(255) NOT NULL,
  `page_title` varchar(255) NOT NULL,
  `device_type` varchar(100) NOT NULL,
  `liked_at` timestamp NULL DEFAULT NULL,
  `reaction_type` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users_likes`
--

INSERT INTO `users_likes` (`id`, `ip_or_name`, `page_title`, `device_type`, `liked_at`, `reaction_type`, `created_at`) VALUES
(36, 'حميد بعلوان', 'قصة الحكيم واختبار الكلمات الثلاث', 'ويندوز', '2025-01-05 23:34:22', 'like', '2025-01-05 23:34:22'),
(37, '105.71.7.27', 'سبع معلومات مغلوطة عن سوس وسكان منطقة سوس', 'موبايل', '2025-01-06 17:41:31', 'like', '2025-01-06 17:41:31'),
(38, '105.71.7.27', 'الإعراب والبناء', 'موبايل', '2025-01-06 17:49:01', 'like', '2025-01-06 17:49:01'),
(39, 'oumaima elmouden', 'Learn HTML In Arabic 2021 - -07 - Headings And Use Cases', 'ويندوز', '2025-01-14 19:29:44', 'love', '2025-01-14 19:29:44'),
(41, 'sirine bellihi', 'سبع معلومات مغلوطة عن سوس وسكان منطقة سوس', 'موبايل', '2025-01-14 21:44:54', 'love', '2025-01-14 21:44:54'),
(43, '102.52.29.248', 'ⵜⵉⵔⴰ - كتاب لتعلم الكتابة بأحرف تيفيناغ', 'ويندوز', '2025-02-26 09:35:04', 'like', '2025-02-26 09:35:04'),
(44, 'sirine bellihi', 'لعنة العنصرية | كيف دعم العلم الممارسات العنصرية على مر التاريخ ؟', 'موبايل', '2025-03-17 15:09:39', 'love', '2025-03-17 15:09:39');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users_likes`
--
ALTER TABLE `users_likes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users_likes`
--
ALTER TABLE `users_likes`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
