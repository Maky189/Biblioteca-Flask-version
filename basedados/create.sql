CREATE TABLE IF NOT EXISTS ESTUDANTES (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NOME VARCHAR(255) NOT NULL,
    NUMERO_ESTUDANTE INT UNSIGNED NOT NULL,
    CURSO VARCHAR(255) NOT NULL,
    CONTACTO VARCHAR(255) NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    LIVROS INT NOT NULL DEFAULT 0,
    PASS VARCHAR(255) NOT NULL DEFAULT '12345'
);

CREATE TABLE IF NOT EXISTS PROFESSORES (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NOME VARCHAR(255) NOT NULL,
    NUMERO_FUNCIONARIO INT UNSIGNED NOT NULL,
    DEPARTAMENTO VARCHAR(255) NOT NULL,
    CONTACTO VARCHAR(255) NOT NULL,
    EMAIL VARCHAR(255) NOT NULL,
    LIVROS INT NOT NULL DEFAULT 0,
    PASS VARCHAR(255) NOT NULL DEFAULT '54321'
);

CREATE TABLE IF NOT EXISTS LIVROS (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    TITULO VARCHAR(255) NOT NULL,
    AUTOR VARCHAR(255) NOT NULL,
    ANO INT UNSIGNED NOT NULL,
    ISBN VARCHAR(255) NOT NULL,
    CATEGORIA VARCHAR(255) NOT NULL,
    NUMERO_COPIAS INT NOT NULL
);

CREATE TABLE IF NOT EXISTS EMPRESTIMOS (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ALUNO_ID INT DEFAULT NULL,
    PROFESSOR_ID INT DEFAULT NULL,
    LIVRO_ID INT NOT NULL,
    DATA_ENTRADA DATE NOT NULL,
    DATA_SAIDA DATE NOT NULL,
    FOREIGN KEY(ALUNO_ID) REFERENCES ESTUDANTES(ID),
    FOREIGN KEY (PROFESSOR_ID) REFERENCES PROFESSORES(ID)
);

ALTER TABLE EMPRESTIMOS
MODIFY COLUMN DATA_SAIDA DATE;

INSERT INTO LIVROS (TITULO, AUTOR, ANO, ISBN, CATEGORIA, NUMERO_COPIAS) VALUES
('Clean Code', 'Robert C. Martin', 2008, '9780132350884', 'Programming', 5),
('The Pragmatic Programmer', 'Andrew Hunt', 1999, '9780201616224', 'Programming', 3),
('Introduction to Algorithms', 'Thomas H. Cormen', 2009, '9780262033848', 'Programming', 4),
('Design Patterns', 'Erich Gamma', 1994, '9780201633610', 'Programming', 2),
('You Don’t Know JS', 'Kyle Simpson', 2014, '9781491904244', 'Programming', 6),
('Refactoring', 'Martin Fowler', 1999, '9780201485677', 'Programming', 5),
('Code Complete', 'Steve McConnell', 2004, '9780735619678', 'Programming', 4),
('The Mythical Man-Month', 'Frederick P. Brooks Jr.', 1975, '9780201835953', 'Programming', 3),
('The Art of Computer Programming', 'Donald E. Knuth', 1968, '9780201896831', 'Programming', 2),
('Structure and Interpretation of Computer Programs', 'Harold Abelson', 1996, '9780262510874', 'Programming', 4),
('Algorithms', 'Robert Sedgewick', 1983, '9780321573513', 'Programming', 3),
('Artificial Intelligence: A Modern Approach', 'Stuart Russell', 1995, '9780136042594', 'Programming', 2),
('Computer Networks', 'Andrew S. Tanenbaum', 1981, '9780132126953', 'Networking', 5),
('Operating System Concepts', 'Abraham Silberschatz', 1982, '9780470128725', 'Operating Systems', 4),
('Database System Concepts', 'Abraham Silberschatz', 1986, '9780073523323', 'Databases', 3);

INSERT INTO ESTUDANTES (NOME, NUMERO_ESTUDANTE, CURSO, CONTACTO, EMAIL, LIVROS) VALUES
('Marcos', 12345, 'Engenharia Informatica', '5833119', 'maky188pgt555@gmail.com', 0),
('Leonardo', 12346, 'Engenharia Informatica', '9970507', 'lf714422@gmail.com', 0),
('Jose', 12347, 'Engenharia Informatica', '5805315', 'jose@gay.com', 0),
('Ana', 12348, 'Engenharia Informatica', '5805316', 'ana@example.com', 0),
('Carlos', 12349, 'Engenharia Informatica', '5805317', 'carlos@example.com', 0),
('Beatriz', 12350, 'Engenharia Informatica', '5805318', 'beatriz@example.com', 0),
('Daniel', 12351, 'Engenharia Informatica', '5805319', 'daniel@example.com', 0),
('Eduardo', 12352, 'Engenharia Informatica', '5805320', 'eduardo@example.com', 0),
('Fernanda', 12353, 'Engenharia Informatica', '5805321', 'fernanda@example.com', 0),
('Gabriel', 12354, 'Engenharia Informatica', '5805322', 'gabriel@example.com', 0);

INSERT INTO PROFESSORES (NOME, NUMERO_FUNCIONARIO, DEPARTAMENTO, CONTACTO, EMAIL, LIVROS) VALUES
('Emmanuel', 54321, 'Computer Science', '987-654-3210', 'emmanuel@mestre.com', 0),
('Joao', 54322, 'Information Systems', '987-654-3211', 'joao@leiohm.com', 0),
('Elisangela', 54323, 'Software Engineering', '987-654-3212', 'elisangela@matematica.com', 0),
('Helena', 54324, 'Computer Science', '987-654-3213', 'helena@example.com', 0),
('Igor', 54325, 'Information Systems', '987-654-3214', 'igor@example.com', 0),
('Juliana', 54326, 'Software Engineering', '987-654-3215', 'juliana@example.com', 0),
('Lucas', 54327, 'Computer Science', '987-654-3216', 'lucas@example.com', 0),
('Mariana', 54328, 'Information Systems', '987-654-3217', 'mariana@example.com', 0),
('Nicolas', 54329, 'Software Engineering', '987-654-3218', 'nicolas@example.com', 0),
('Olivia', 54330, 'Computer Science', '987-654-3219', 'olivia@example.com', 0);

INSERT INTO EMPRESTIMOS (ALUNO_ID, LIVRO_ID, DATA_ENTRADA, DATA_SAIDA) VALUES
(1, 1, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(2, 2, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(3, 3, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(4, 4, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(5, 5, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(6, 6, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(7, 7, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(8, 8, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(9, 9, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(10, 10, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(1, 11, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(2, 12, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(3, 13, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(4, 14, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY)),
(5, 15, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 15 DAY));

DELIMITER //

CREATE TRIGGER before_insert_emprestimos
BEFORE INSERT ON EMPRESTIMOS
FOR EACH ROW
BEGIN
    DECLARE user_type VARCHAR(255);
    
    SELECT 'ESTUDANTE' INTO user_type
    FROM ESTUDANTES
    WHERE ID = NEW.ALUNO_ID;
    
    IF user_type IS NOT NULL THEN
        SET NEW.DATA_SAIDA = DATE_ADD(NEW.DATA_ENTRADA, INTERVAL 15 DAY);
    ELSE
        SELECT 'PROFESSOR' INTO user_type
        FROM PROFESSORES
        WHERE ID = NEW.PROFESSOR_ID;
        
        IF user_type IS NOT NULL THEN
            SET NEW.DATA_SAIDA = DATE_ADD(NEW.DATA_ENTRADA, INTERVAL 30 DAY);
        END IF;
    END IF;
END;

//

DELIMITER ;

