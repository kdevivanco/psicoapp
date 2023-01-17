from app.models.connection import connectToMySQL

class CreateTables:

    @classmethod
    def create_tables(cls):
        queries = [
        '''
        CREATE TABLE IF NOT EXISTS `suscribe` (
            `id_suscribe` INT NOT NULL AUTO_INCREMENT,
            `email` VARCHAR(255) NOT NULL,
            `created_at` DATETIME NULL DEFAULT NOW(),
            `updated_at` DATETIME NULL DEFAULT NOW(),
            PRIMARY KEY (`id_suscribe`))
        ENGINE = InnoDB;
        ''',
        '''
        CREATE TABLE IF NOT EXISTS `contacts` (
            `id_contact` INT NOT NULL AUTO_INCREMENT,
            `date` DATETIME NOT NULL,
            `name` VARCHAR(255) NOT NULL,
            `email` VARCHAR(255) NOT NULL,
            `cell` BIGINT NULL,
            `message` TEXT(1000) NOT NULL,
            `created_at` DATETIME NULL DEFAULT NOW(),
            `updated_at` DATETIME NULL DEFAULT NOW(),
            PRIMARY KEY (`id_contact`))
        ENGINE = InnoDB;
        '''

        ]
        for query in queries:
            connectToMySQL().query_db(query)
