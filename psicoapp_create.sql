-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema psicoapp
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `psicoapp` ;

-- -----------------------------------------------------
-- Schema psicoapp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `psicoapp` DEFAULT CHARACTER SET utf8 ;
USE `psicoapp` ;

-- -----------------------------------------------------
-- Table `psicoapp`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`location` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(255) NOT NULL,
  `district` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `psicoapp`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `psicoapp`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `linkedin` VARCHAR(255) NULL,
  `age` INT NULL,
  `gender` VARCHAR(45) NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `type_of_account` TINYINT(2) NOT NULL,
  `modalidad` VARCHAR(255) NOT NULL,
  `cdr` VARCHAR(255) NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `psicoapp`.`address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`address` (
  `location_id`  INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`location_id`, `user_id`),
    FOREIGN KEY (`location_id`)
    REFERENCES `psicoapp`.`location` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`user_id`)
    REFERENCES `psicoapp`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `psicoapp`.`education`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`education` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `school_name` VARCHAR(255) NOT NULL,
  `title_name` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `therapist_id` INT NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`therapist_id`)
    REFERENCES `psicoapp`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);



-- -----------------------------------------------------
-- Table `psicoapp`.`mensajes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`mensajes` (
 `id` INT NOT NULL AUTO_INCREMENT,
  `sender_id` INT NOT NULL,
  `reciever_id` INT NOT NULL,
  `text` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `status` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`sender_id`)
    REFERENCES `psicoapp`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`reciever_id`)
    REFERENCES `psicoapp`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `psicoapp`.`publications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`publications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title`  VARCHAR(255)  NOT NULL,
  `description`  VARCHAR(400) NOT NULL,
  `created_at`  DATETIME NOT NULL,
  `file` VARCHAR(255) NULL,
  `publication_link` TEXT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`)
    REFERENCES `psicoapp`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `psicoapp`.`articles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`articles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `body` TEXT NOT NULL,
  `created_at` VARCHAR(255) NOT NULL,
  `img_filename` VARCHAR(255) NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`)
    REFERENCES `psicoapp`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `psicoapp`.`user_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`user_categories` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `category_id`),
    FOREIGN KEY (`user_id`)
    REFERENCES `psicoapp`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`category_id`)
    REFERENCES `psicoapp`.`category` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `psicoapp`.`publication_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`publication_categories` (
  `publication_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`publication_id`, `category_id`),
    FOREIGN KEY (`publication_id`)
    REFERENCES `psicoapp`.`publications` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`category_id`)
    REFERENCES `psicoapp`.`category` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `psicoapp`.`article_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `psicoapp`.`article_categories` (
  `article_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`article_id`, `category_id`),
    FOREIGN KEY (`article_id`)
    REFERENCES `psicoapp`.`articles` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (`category_id`)
    REFERENCES `psicoapp`.`category` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

ALTER TABLE `psicoapp`.`users` 
ADD COLUMN `confirmation_hash` VARCHAR(6) NULL AFTER `cdr`,
ADD COLUMN `validated` TINYINT NULL AFTER `confirmation_hash`,
CHANGE COLUMN `type_of_account` `type` TINYINT NOT NULL ;


ALTER TABLE `psicoapp`.`users` 
ADD COLUMN `metodo` VARCHAR(255) NULL AFTER `validated`;


ALTER TABLE `psicoapp`.`users` 
CHANGE COLUMN `modalidad` `modalidad` VARCHAR(255) NULL ;


ALTER TABLE `psicoapp`.`category` 
RENAME TO  `psicoapp`.`categories` ;

INSERT INTO categories (name) VALUES ("Anxiety"),("Depression"),("Stress"),("Trauma"),("PTSD"),("Grief and Loss"),("Eating Disorders"),("Obsessive-Compulsive Disorder (OCD)"),("Attention-Deficit Hyperactivity Disorder (ADHD)"),("Autism Spectrum Disorder"),("Borderline Personality Disorder"),("Schizophrenia"),("Bipolar Disorder"),("Dissociative Identity Disorder"),("Substance Abuse"),("Addiction"),("Anger Management"),("Relationship Issues"),("Marriage and Couples Counseling"),("Family Therapy"),("Parenting"),("Child Psychology"),("Adolescent Psychology"),("Aging and Geriatric Psychology"),("Career Counseling"),("Workplace Issues"),("Educational Psychology"),("Sports Psychology"),("Forensic Psychology"),("Military Psychology"),("Neuropsychology"),("Evolutionary Psychology"),("Cross-Cultural Psychology"),("Social Psychology"),("Cognitive Psychology"),("Developmental Psychology"),("Abnormal Psychology"),("Personality Psychology"),("Positive Psychology"),("Clinical Psychology"),("Counseling Psychology"),("Community Psychology"),("Health Psychology"),("Rehabilitation Psychology"),("School Psychology"),("Industrial-Organizational Psychology"),("Gender and Sexuality"),("Environmental Psychology"),("Consumer Psychology"),("Political Psychology"),("Media Psychology"),("Spirituality and Religion"),("Technology and Psychology"),("Police and Law Enforcement Psychology"),("Animals and Psychology"),("Disaster and Emergency Psychology"),("Fitness and Exercise Psychology"),("Food and Nutrition Psychology"),("Hospital and Medical Psychology");

ALTER TABLE `psicoapp`.`articles` 
ADD COLUMN `bibliography` TEXT NULL AFTER `user_id`;

ALTER TABLE `psicoapp`.`articles` 
ADD COLUMN `subtitle` VARCHAR(400) NOT NULL AFTER `bibliography`;

ALTER TABLE `psicoapp`.`users` 
ADD COLUMN `city` VARCHAR(255) NULL AFTER `metodo`;
