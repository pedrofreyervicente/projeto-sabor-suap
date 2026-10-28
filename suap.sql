-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 28/10/2026 às 03:06
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `suap`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `alunos`
--

CREATE TABLE `alunos` (
  `idAluno` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `data` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- --------------------------------------------------------

--
-- Estrutura para tabela `disciplinas`
--

CREATE TABLE `disciplinas` (
  `idDisciplina` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;



-- --------------------------------------------------------

--
-- Estrutura para tabela `notas`
--

CREATE TABLE `notas` (
  `idNotas` int(11) NOT NULL,
  `idProfessor` int(11) NOT NULL,
  `idAluno` int(11) NOT NULL,
  `idDisciplina` int(11) NOT NULL,
  `idTurma` int(11) NOT NULL,
  `nota` decimal(4,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Estrutura para tabela `professores`
--

CREATE TABLE `professores` (
  `idProfessor` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Estrutura para tabela `relacionamentoaluno`
--

CREATE TABLE `relacionamentoaluno` (
  `idAluno` int(11) NOT NULL,
  `idTurma` int(11) NOT NULL,
  `idDisciplina` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Estrutura para tabela `turmas`
--

CREATE TABLE `turmas` (
  `idTurma` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `ano` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `alunos`
--
ALTER TABLE `alunos`
  ADD PRIMARY KEY (`idAluno`);

--
-- Índices de tabela `disciplinas`
--
ALTER TABLE `disciplinas`
  ADD PRIMARY KEY (`idDisciplina`);

--
-- Índices de tabela `notas`
--
ALTER TABLE `notas`
  ADD PRIMARY KEY (`idNotas`),
  ADD KEY `fk_notas_professor` (`idProfessor`),
  ADD KEY `fk_notas_aluno` (`idAluno`),
  ADD KEY `fk_notas_disciplina` (`idDisciplina`),
  ADD KEY `fk_notas_turma` (`idTurma`);

--
-- Índices de tabela `professores`
--
ALTER TABLE `professores`
  ADD PRIMARY KEY (`idProfessor`);

--
-- Índices de tabela `relacionamentoaluno`
--
ALTER TABLE `relacionamentoaluno`
  ADD PRIMARY KEY (`idAluno`,`idTurma`,`idDisciplina`),
  ADD KEY `fk_ra_turma` (`idTurma`),
  ADD KEY `fk_ra_disciplina` (`idDisciplina`);

--
-- Índices de tabela `relacionamentoprofessor`
--
ALTER TABLE `relacionamentoprofessor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_turma_disciplina_prof` (`idTurma`,`idDisciplina`),
  ADD KEY `fk_rp_disciplina` (`idDisciplina`),
  ADD KEY `fk_rp_professor` (`idProfessor`);

--
-- Índices de tabela `relacionamentoturma`
--
ALTER TABLE `relacionamentoturma`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_turma_disciplina` (`idTurma`,`idDisciplina`),
  ADD KEY `fk_rt_disciplina` (`idDisciplina`);

--
-- Índices de tabela `turmas`
--
ALTER TABLE `turmas`
  ADD PRIMARY KEY (`idTurma`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `alunos`
--
ALTER TABLE `alunos`
  MODIFY `idAluno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=124;

--
-- AUTO_INCREMENT de tabela `disciplinas`
--
ALTER TABLE `disciplinas`
  MODIFY `idDisciplina` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de tabela `notas`
--
ALTER TABLE `notas`
  MODIFY `idNotas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT de tabela `professores`
--
ALTER TABLE `professores`
  MODIFY `idProfessor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de tabela `relacionamentoprofessor`
--
ALTER TABLE `relacionamentoprofessor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=203;

--
-- AUTO_INCREMENT de tabela `relacionamentoturma`
--
ALTER TABLE `relacionamentoturma`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT de tabela `turmas`
--
ALTER TABLE `turmas`
  MODIFY `idTurma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `notas`
--
ALTER TABLE `notas`
  ADD CONSTRAINT `fk_notas_aluno` FOREIGN KEY (`idAluno`) REFERENCES `alunos` (`idAluno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notas_disciplina` FOREIGN KEY (`idDisciplina`) REFERENCES `disciplinas` (`idDisciplina`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notas_professor` FOREIGN KEY (`idProfessor`) REFERENCES `professores` (`idProfessor`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_notas_turma` FOREIGN KEY (`idTurma`) REFERENCES `turmas` (`idTurma`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `relacionamentoaluno`
--
ALTER TABLE `relacionamentoaluno`
  ADD CONSTRAINT `fk_ra_aluno` FOREIGN KEY (`idAluno`) REFERENCES `alunos` (`idAluno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_ra_disciplina` FOREIGN KEY (`idDisciplina`) REFERENCES `disciplinas` (`idDisciplina`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_ra_turma` FOREIGN KEY (`idTurma`) REFERENCES `turmas` (`idTurma`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `relacionamentoprofessor`
--
ALTER TABLE `relacionamentoprofessor`
  ADD CONSTRAINT `fk_rp_disciplina` FOREIGN KEY (`idDisciplina`) REFERENCES `disciplinas` (`idDisciplina`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_rp_professor` FOREIGN KEY (`idProfessor`) REFERENCES `professores` (`idProfessor`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_rp_turma` FOREIGN KEY (`idTurma`) REFERENCES `turmas` (`idTurma`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `relacionamentoturma`
--
ALTER TABLE `relacionamentoturma`
  ADD CONSTRAINT `fk_rt_disciplina` FOREIGN KEY (`idDisciplina`) REFERENCES `disciplinas` (`idDisciplina`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_rt_turma` FOREIGN KEY (`idTurma`) REFERENCES `turmas` (`idTurma`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
