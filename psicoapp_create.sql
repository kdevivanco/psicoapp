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


ALTER TABLE `psicoapp`.`articles` 
ADD COLUMN `bibliography` TEXT NULL AFTER `user_id`;

ALTER TABLE `psicoapp`.`articles` 
ADD COLUMN `subtitle` VARCHAR(400) NOT NULL AFTER `bibliography`;

ALTER TABLE `psicoapp`.`users` 
ADD COLUMN `city` VARCHAR(255) NULL AFTER `metodo`;


ALTER TABLE `psicoapp`.`publications` 
ADD COLUMN `publisher` VARCHAR(255) NOT NULL AFTER `user_id`,
ADD COLUMN `date` DATE NOT NULL AFTER `publisher`;
ALTER TABLE `psicoapp`.`publications` 
CHANGE COLUMN `file` `file` VARCHAR(255) NOT NULL ,
CHANGE COLUMN `publication_link` `publication_link` TEXT NOT NULL ;


INSERT INTO categories (name) VALUES ("Anxiety"),("Depression"),("Stress"),("Trauma"),("PTSD"),("Grief and Loss"),("Eating Disorders"),("Obsessive-Compulsive Disorder (OCD)"),("Attention-Deficit Hyperactivity Disorder (ADHD)"),("Autism Spectrum Disorder"),("Borderline Personality Disorder"),("Schizophrenia"),("Bipolar Disorder"),("Dissociative Identity Disorder"),("Substance Abuse"),("Addiction"),("Anger Management"),("Relationship Issues"),("Marriage and Couples Counseling"),("Family Therapy"),("Parenting"),("Child Psychology"),("Adolescent Psychology"),("Aging and Geriatric Psychology"),("Career Counseling"),("Workplace Issues"),("Educational Psychology"),("Sports Psychology"),("Forensic Psychology"),("Military Psychology"),("Neuropsychology"),("Evolutionary Psychology"),("Cross-Cultural Psychology"),("Social Psychology"),("Cognitive Psychology"),("Developmental Psychology"),("Abnormal Psychology"),("Personality Psychology"),("Positive Psychology"),("Clinical Psychology"),("Counseling Psychology"),("Community Psychology"),("Health Psychology"),("Rehabilitation Psychology"),("School Psychology"),("Industrial-Organizational Psychology"),("Gender and Sexuality"),("Environmental Psychology"),("Consumer Psychology"),("Political Psychology"),("Media Psychology"),("Spirituality and Religion"),("Technology and Psychology"),("Police and Law Enforcement Psychology"),("Animals and Psychology"),("Disaster and Emergency Psychology"),("Fitness and Exercise Psychology"),("Food and Nutrition Psychology"),("Hospital and Medical Psychology");

--- inserts ---
INSERT INTO location (city, district) VALUES 
('AMAZONAS', 'CHACHAPOYAS'),
('AMAZONAS', 'ASUNCION'),
('AMAZONAS', 'BALSAS'),
('AMAZONAS', 'CHETO'),
('AMAZONAS', 'CHILIQUIN'),
('AMAZONAS', 'CHUQUIBAMBA'),
('AMAZONAS', 'HUANCAS'),
('AMAZONAS', 'LA JALCA'),
('AMAZONAS', 'LEIMEBAMBA'),
('AMAZONAS', 'MAGDALENA'),
('AMAZONAS', 'MONTEVIDEO'),
('AMAZONAS', 'QUINJALCA'),
('AMAZONAS', 'SAN ISIDRO DE MAINO'),
('AMAZONAS', 'SONCHE'),
('AMAZONAS', 'BAGUA'),
('AMAZONAS', 'LA PECA'),
('AMAZONAS', 'ARAMANGO'),
('AMAZONAS', 'EL PARCO'),
('AMAZONAS', 'IMAZA'),
('AMAZONAS', 'BONGARA'),
('AMAZONAS', 'JUMBILLA'),
('AMAZONAS', 'CHURUJA'),
('AMAZONAS', 'COROSHA'),
('AMAZONAS', 'CUISPES'),
('AMAZONAS', 'JAZAN'),
('AMAZONAS', 'RECTA'),
('AMAZONAS', 'SAN CARLOS'),
('AMAZONAS', 'SHIPASBAMBA'),
('AMAZONAS', 'YAMBRASBAMBA'),
('AMAZONAS', 'CONDORCANQUI'),
('AMAZONAS', 'NIEVA'),
('AMAZONAS', 'EL CENEPA'),
('AMAZONAS', 'RIO SANTIAGO'),
('AMAZONAS', 'LUYA'),
('AMAZONAS', 'LAMUD'),
('AMAZONAS', 'CAMPORREDONDO'),
('AMAZONAS', 'COLCAMAR'),
('AMAZONAS', 'CONILA'),
('AMAZONAS', 'INGUILPATA'),
('AMAZONAS', 'LONGUITA'),
('AMAZONAS', 'LUYA'),
('AMAZONAS', 'MARIA'),
('AMAZONAS', 'OCALLI'),
('AMAZONAS', 'PROVIDENCIA'),
('AMAZONAS', 'SAN CRISTOBAL'),
('AMAZONAS', 'SAN FRANCISCO DEL YESO'),
('AMAZONAS', 'SAN JUAN DE LOPECANCHA'),
('AMAZONAS', 'SANTA CATALINA'),
('AMAZONAS', 'SANTO TOMAS'),
('AMAZONAS', 'TINGO'),
('AMAZONAS', 'TRITA'),
('AMAZONAS', 'RODRIGUEZ DE MENDOZA'),
('AMAZONAS', 'SAN NICOLAS'),
('AMAZONAS', 'CHIRIMOTO'),
('AMAZONAS', 'HUAMBO'),
('AMAZONAS', 'LIMABAMBA'),
('AMAZONAS', 'LONGAR'),
('AMAZONAS', 'MARISCAL BENAVIDES'),
('AMAZONAS', 'MILPUC'),
('AMAZONAS', 'OMIA'),
('AMAZONAS', 'SANTA ROSA'),
('AMAZONAS', 'TOTORA'),
('AMAZONAS', 'UTCUBAMBA'),
('AMAZONAS', 'BAGUA GRANDE'),
('AMAZONAS', 'CAJARURO'),
('AMAZONAS', 'CUMBA'),
('AMAZONAS', 'EL MILAGRO'),
('AMAZONAS', 'JAMALCA'),
('AMAZONAS', 'LONYA GRANDE'),
('AMAZONAS', 'YAMON');

INSERT INTO location (city, district) VALUES 
('ANCASH', 'AIJA'),
('ANCASH', 'CORIS'),
('ANCASH', 'HUACLLAN'),
('ANCASH', 'LA MERCED'),
('ANCASH', 'SUCCHA'),
('ANCASH', 'ACZO'),
('ANCASH', 'CHACCHO'),
('ANCASH', 'CHINGAS'),
('ANCASH', 'LLAMELLIN'),
('ANCASH', 'MIRGAS'),
('ANCASH', 'SAN JUAN DE RONTOY'),
('ANCASH', 'ACOCHACA'),
('ANCASH', 'CHACAS'),
('ANCASH', 'ABELARDO PARDO LEZAMETA'),
('ANCASH', 'ANTONIO RAYMONDI'),
('ANCASH', 'AQUIA'),
('ANCASH', 'CAJACAY'),
('ANCASH', 'CANIS'),
('ANCASH', 'CHIQUIAN'),
('ANCASH', 'COLQUIOC'),
('ANCASH', 'HUALLANCA'),
('ANCASH', 'HUASTA'),
('ANCASH', 'HUAYLLACAYAN'),
('ANCASH', 'LA PRIMAVERA'),
('ANCASH', 'MANGAS'),
('ANCASH', 'PACLLON'),
('ANCASH', 'SAN MIGUEL DE CORPANGQUI'),
('ANCASH', 'TICLLOS'),
('ANCASH', 'ACOPAMPA'),
('ANCASH', 'AMASHCA'),
('ANCASH', 'ANTA'),
('ANCASH', 'ATAQUERO'),
('ANCASH', 'CARHUAZ'),
('ANCASH', 'MARCARA'),
('ANCASH', 'PARIAHUANCA'),
('ANCASH', 'SAN MIGUEL DE ACO'),
('ANCASH', 'SHILLA'),
('ANCASH', 'TINCO'),
('ANCASH', 'YUNGAR'),
('ANCASH', 'SAN LUIS'),
('ANCASH', 'SAN NICOLAS'),
('ANCASH', 'YAUYA'),
('ANCASH', 'BUENA VISTA ALTA'),
('ANCASH', 'CASMA'),
('ANCASH', 'COMANDANTE NOEL'),
('ANCASH', 'YAUTAN'),
('ANCASH', 'ACO'),
('ANCASH', 'BAMBAS'),
('ANCASH', 'CORONGO'),
('ANCASH', 'CUSCA'),
('ANCASH', 'LA PAMPA'),
('ANCASH', 'YANAC'),
('ANCASH', 'YUPAN'),
('ANCASH', 'COCHABAMBA'),
('ANCASH', 'COLCABAMBA'),
('ANCASH', 'HUANCHAY'),
('ANCASH', 'HUARAZ'),
('ANCASH', 'INDEPENDENCIA'),
('ANCASH', 'JANGAS'),
('ANCASH', 'LA LIBERTAD'),
('ANCASH', 'OLLEROS'),
('ANCASH', 'PAMPAS'),
('ANCASH', 'PARIACOTO'),
('ANCASH', 'PIRA'),
('ANCASH', 'TARICA'),
('ANCASH', 'ANRA'),
('ANCASH', 'CAJAY'),
('ANCASH', 'CHAVIN DE HUANTAR'),
('ANCASH', 'HUACACHI'),
('ANCASH', 'HUACCHIS'),
('ANCASH', 'HUACHIS'),
('ANCASH', 'HUANTAR'),
('ANCASH', 'HUARI'),
('ANCASH', 'PAUCAS'),
('ANCASH', 'PONTO'),
('ANCASH', 'RAHUAPAMPA'),
('ANCASH', 'RAPAYAN'),
('ANCASH', 'SAN MARCOS'),
('ANCASH', 'SAN PEDRO DE CHANA'),
('ANCASH', 'UCO'),
('ANCASH', 'COCHAPETI'),
('ANCASH', 'CPEBRAS'),
('ANCASH', 'HUARMEY'),
('ANCASH', 'HUAYAN'),
('ANCASH', 'MALVAS'),
('ANCASH', 'CARAZ'),
('ANCASH', 'HUALLANCA'),
('ANCASH', 'HUATA'),
('ANCASH', 'HUAYLAS'),
('ANCASH', 'MATO'),
('ANCASH', 'PAMPAROMAS'),
('ANCASH', 'PUEBLO LIBRE'),
('ANCASH', 'SANTA CRUZ'),
('ANCASH', 'SANTO TORIBIO'),
('ANCASH', 'YURACMARCA'),
('ANCASH', 'CASCA'),
('ANCASH', 'ELEAZAR GUMAN BARRON'),
('ANCASH', 'FIDEL OLIVAS ESCUDERO'),
('ANCASH', 'LLAMA'),
('ANCASH', 'LLUMPA'),
('ANCASH', 'LUCMA'),
('ANCASH', 'MUSGA'),
('ANCASH', 'PISCOBAMBA'),
('ANCASH', 'ACAS'),
('ANCASH', 'CAJAMARQUILLA'),
('ANCASH', 'CARHUAPAMPA'),
('ANCASH', 'COCHAS'),
('ANCASH', 'CONGAS'),
('ANCASH', 'LLIPA'),
('ANCASH', 'OCROS'),
('ANCASH', 'SAN CRISTOBAL DE RAJAN'),
('ANCASH', 'SAN PEDRO'),
('ANCASH', 'SANTIAGO DE CHILCAS'),
('ANCASH', 'BOLGNESI'),
('ANCASH', 'CABANA'),
('ANCASH', 'CONCHUCOS'),
('ANCASH', 'HUACASCHUQUE'),
('ANCASH', 'HUANDOVAL'),
('ANCASH', 'LACABAMBA'),
('ANCASH', 'LLAPO'),
('ANCASH', 'PALLASCA'),
('ANCASH', 'PAMPAS'),
('ANCASH', 'SANTA ROSA'),
('ANCASH', 'TAUCA'),
('ANCASH', 'HUAYLLAN'),
('ANCASH', 'PAROBAMBA'),
('ANCASH', 'POMABAMBA'),
('ANCASH', 'QUINUABAMBA'),
('ANCASH', 'CATAC'),
('ANCASH', 'COTAPARACO'),
('ANCASH', 'HUAYLLAPAMPA'),
('ANCASH', 'LLACLLIN'),
('ANCASH', 'MARCA'),
('ANCASH', 'PAMPAS CHICO'),
('ANCASH', 'PARARIN'),
('ANCASH', 'RECUAY'),
('ANCASH', 'TAPACOCHA'),
('ANCASH', 'TICAPAMPA'),
('ANCASH', 'CACERES DEL PERU'),
('ANCASH', 'CHIMBOTE'),
('ANCASH', 'COISHCO'),
('ANCASH', 'MACATE'),
('ANCASH', 'MORO'),
('ANCASH', 'NEPEÑA'),
('ANCASH', 'NUEVO CHIMBOTE'),
('ANCASH', 'SAMANCO'),
('ANCASH', 'SANTA'),
('ANCASH', 'ACOBAMBA'),
('ANCASH', 'ALFONSO UGARTE'),
('ANCASH', 'CASHAPAMPA'),
('ANCASH', 'CHINGALPO'),
('ANCASH', 'HUAYLLABAMBA'),
('ANCASH', 'QUICHES'),
('ANCASH', 'RAGASH'),
('ANCASH', 'SAN JUAN'),
('ANCASH', 'SICSIBAMBA'),
('ANCASH', 'SIHUAS'),
('ANCASH', 'CASCAPARA'),
('ANCASH', 'MANCOS'),
('ANCASH', 'MATACOTO'),
('ANCASH', 'QUILLO'),
('ANCASH', 'RANRAHIRCA'),
('ANCASH', 'SHUPLUY'),
('ANCASH', 'YANAMA'),
('ANCASH', 'YUNGAY')

INSERT INTO location (city, district) VALUES('APURIMAC','ABANCAY'),('APURIMAC','CHACOCHE'),('APURIMAC','CIRCA'),('APURIMAC','CURAHUASI'),('APURIMAC','HUANIPACA'),('APURIMAC','LAMBRAMA'),('APURIMAC','PICHIRHUA'),('APURIMAC','SAN PEDRO DE CACHORA'),('APURIMAC','TAMBURCO'),('APURIMAC','ANDAHUAYLAS'),('APURIMAC','ANDARAPA'),('APURIMAC','CHIARA'),('APURIMAC','HUANCARAMA'),('APURIMAC','HUANCARAY'),('APURIMAC','HUAYANA'),('APURIMAC','KAQUIABAMBA'),('APURIMAC','KISHUARA'),('APURIMAC','PACOBAMBA'),('APURIMAC','PACUCHA'),('APURIMAC','PAMPACHIRI'),('APURIMAC','POMACOCHA'),('APURIMAC','SAN ANTONIO DE CACHI'),('APURIMAC','SAN JERONIMO'),('APURIMAC','SANMIGUEL DE CHACCRAMPA'),('APURIMAC','SANTA MARIA DE CHICMO'),('APURIMAC','TALAVERA'),('APURIMAC','TUMAY HUARACA'),('APURIMAC','TURPO'),('APURIMAC','ANTABAMBA'),('APURIMAC','EL ORO'),('APURIMAC','HUAQUIRCA'),('APURIMAC','JUAN ESPINOZA MEDRANO'),('APURIMAC','OROPESA'),('APURIMAC','PACHACONAS'),('APURIMAC','SABAINO'),('APURIMAC','CAPAYA'),('APURIMAC','CARAYBAMBA'),('APURIMAC','CHALHUANCA'),('APURIMAC','CHAPIMARCA'),('APURIMAC','COLCABAMBA'),('APURIMAC','COTARUSE'),('APURIMAC','HAUAYLLO'),('APURIMAC','JUSTO APU SAHUARAURA'),('APURIMAC','LUCRE'),('APURIMAC','POCOHUANCA'),('APURIMAC','SAN JUAN DE CHACÑA'),('APURIMAC','SAÑAYCA'),('APURIMAC','SORAYA'),('APURIMAC','TAPAIRIHUA'),('APURIMAC','TINTAY'),('APURIMAC','TORAYA'),('APURIMAC','YANACA'),('APURIMAC','CHALLHUAHUACHO'),('APURIMAC','COTABAMBAS'),('APURIMAC','COYLLURQUI'),('APURIMAC','HAQUIRA'),('APURIMAC','MARA'),('APURIMAC','TAMBOBAMBA'),('APURIMAC','ANCO HUALLO'),('APURIMAC','CHINCHEROS'),('APURIMAC','COCHARCAS'),('APURIMAC','HUACCANA'),('APURIMAC','OCOBAMBA'),('APURIMAC','ONGOY'),('APURIMAC','RANRACANCHA'),('APURIMAC','URANMARCA'),('APURIMAC','CHUQUIBAMBILLA'),('APURIMAC','CURASCO'),('APURIMAC','CURPAHUASI'),('APURIMAC','GAMARRA'),('APURIMAC','HUAYLLATI'),('APURIMAC','MAMARA'),('APURIMAC','MICAELA BASTIDAS'),('APURIMAC','PATAYPAMPA'),('APURIMAC','PROGRESO'),('APURIMAC','SAN ANTONIO'),('APURIMAC','SANTA ROSA'),('APURIMAC','TURPAY'),('APURIMAC','VILCABAMBA'),('APURIMAC','VIRUNDO')


