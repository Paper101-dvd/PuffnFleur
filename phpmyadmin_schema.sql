-- phpMyAdmin SQL Dump
-- Version: 5.2.x
-- Database: puffnfleur
-- Purpose: create tables for admin auth, bookings CRUD, and package CRUD

CREATE DATABASE IF NOT EXISTS puffnfleur
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE puffnfleur;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL,
  email VARCHAR(120) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_users_username (username),
  UNIQUE KEY uq_users_email (email),
  KEY idx_users_username (username),
  KEY idx_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS packages (
  id VARCHAR(20) NOT NULL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  delivery TINYINT(1) NOT NULL DEFAULT 1,
  image VARCHAR(200) DEFAULT NULL,
  features_json TEXT NOT NULL,
  sort_order INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS bookings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(150) NOT NULL,
  email VARCHAR(120) NOT NULL,
  phone VARCHAR(30) NOT NULL,
  event_type VARCHAR(80) NOT NULL,
  preferred_package VARCHAR(20) DEFAULT NULL,
  custom_package_details TEXT DEFAULT NULL,
  event_date VARCHAR(20) NOT NULL,
  event_location VARCHAR(200) NOT NULL,
  additional_notes TEXT DEFAULT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'new',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_bookings_created_at (created_at),
  KEY idx_bookings_event_type (event_type),
  KEY idx_bookings_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO packages (id, name, price, delivery, image, features_json, sort_order)
VALUES
  ('A', 'Basic', 270.00, 1, 'basic.jpg', '["One Backdrop (color of your choice)", "Balloon garland with up to 3 colors", "Custom Happy Birthday Vinyl or LED sign"]', 1),
  ('B', 'Standard', 330.00, 1, 'standard.jfif', '["Two Arch Backdrop (color of your choice)", "Balloon garland with up to 3 colors", "Custom Happy Birthday Vinyl or LED sign"]', 2),
  ('C', 'Deluxe', 300.00, 1, 'deluxe.png', '["One Backdrop (color of your choice)", "Balloon garland with up to 3 colors", "Custom Happy Birthday Vinyl or LED sign", "One character prop (3ft-4ft)", "+$50 for additional backdrop"]', 3)
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  price = VALUES(price),
  delivery = VALUES(delivery),
  image = VALUES(image),
  features_json = VALUES(features_json),
  sort_order = VALUES(sort_order);
