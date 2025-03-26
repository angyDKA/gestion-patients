-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Mer 26 Mars 2025 à 14:54
-- Version du serveur :  5.6.17
-- Version de PHP :  5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `hopital`
--

-- --------------------------------------------------------

--
-- Structure de la table `patients`
--

CREATE TABLE IF NOT EXISTS `patients` (
  `matricule` varchar(10) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `remarque` text,
  PRIMARY KEY (`matricule`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `patients`
--

INSERT INTO `patients` (`matricule`, `nom`, `prenom`, `age`, `adresse`, `telephone`, `remarque`) VALUES
('24SJI1', 'DJUISSI KENMOE', 'Ange Nolwen', 21, '75015, Paris', '0670452686', 'Malade'),
('24SJI2', 'KENMOE DJUISSI', 'Ange Nolwen', 21, '75001, Paris', '0670452686', 'Malade'),
('24SJI3', 'DJUISSI KENMOE', 'Nolwen Ange', 21, '75004, Paris', '0670452686', 'En forme '),
('24SJI4', 'ANGE NOLWEN', 'Djuissi Kenmoe', 21, '75002,Paris', '0670452686', 'Hospitalisé');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
