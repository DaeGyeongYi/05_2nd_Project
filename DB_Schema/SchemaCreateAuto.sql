CREATE TABLE `학군` (
  `학군ID` int,
  `법정동코드` int PRIMARY KEY,
  `비평준화여부` boolean,
  `전체학령인구` int,
  `교원1인당 학생수` int,
  `중학교 학업중단자수` int,
  `고등학교 학업중단자수` int
);

CREATE TABLE `교육청` (
  `교육청코드` int PRIMARY KEY,
  `학군ID` int,
  `교육청명` varchar(255),
  `시도명` varchar(255),
  `예산` int
);

CREATE TABLE `학원` (
  `학원ID` int PRIMARY KEY,
  `학군ID` int,
  `법정동명` varchar(255),
  `학원명` varchar(255),
  `계열명` varchar(255),
  `주소` varchar(255),
  `정원합계` int
);

CREATE TABLE `강사` (
  `강사채용ID` int PRIMARY KEY,
  `학군ID` int,
  `법정동명` varchar(255),
  `학원명` varchar(255),
  `과목명` varchar(255)
);

CREATE TABLE `지역` (
  `법정동코드` int PRIMARY KEY,
  `시도명` varchar(255),
  `법정동명` varchar(255)
);

CREATE TABLE `유초등학교` (
  `학교ID` int PRIMARY KEY,
  `학군ID` int,
  `유초등학교명` varchar(255),
  `학교종류` varchar(255)
);

CREATE TABLE `중학교` (
  `학교ID` int PRIMARY KEY,
  `학군ID` int,
  `중학교명` varchar(255),
  `학교종류` varchar(255),
  `특목고진학자수` int
);

CREATE TABLE `고등학교` (
  `학교ID` int PRIMARY KEY,
  `학군ID` int,
  `고등학교명` varchar(255),
  `학교종류` varchar(255),
  `서울대합격자수` int
);

CREATE TABLE `지하철` (
  `지하철역번호` int PRIMARY KEY,
  `지하철역사명` varchar(255),
  `노선명` varchar(255),
  `노선번호` varchar(255),
  `환승역구분` varchar(255),
  `환승노선개수` int,
  `환승노선번호` varchar(255),
  `환승노선명` varchar(255),
  `법정동코드` int
);

CREATE TABLE `버스정류장` (
  `버스정류장ID` int PRIMARY KEY,
  `법정동코드` int,
  `버스정류장명` varchar(255)
);

CREATE TABLE `유흥업소` (
  `유흥업소ID` int PRIMARY KEY,
  `법정동코드` int,
  `사업장명` varchar(255),
  `구분명` varchar(255)
);

CREATE TABLE `가구` (
  `가구ID` int PRIMARY KEY,
  `법정동코드` int,
  `건강보험료` int,
  `급여인원` int,
  `급여금액` int
);

CREATE TABLE `부동산` (
  `부동산ID` int PRIMARY KEY,
  `법정동코드` int,
  `거래금액` int,
  `건축년도` varchar(255),
  `계약날짜` datetime,
  `아파트명` varchar(255),
  `면적` int,
  `층` int
);

ALTER TABLE `학군` ADD FOREIGN KEY (`법정동코드`) REFERENCES `지역` (`법정동코드`);

ALTER TABLE `버스정류장` ADD FOREIGN KEY (`법정동코드`) REFERENCES `지역` (`법정동코드`);

ALTER TABLE `지하철` ADD FOREIGN KEY (`법정동코드`) REFERENCES `지역` (`법정동코드`);

ALTER TABLE `유흥업소` ADD FOREIGN KEY (`법정동코드`) REFERENCES `지역` (`법정동코드`);

ALTER TABLE `학원` ADD FOREIGN KEY (`학군ID`) REFERENCES `학군` (`학군ID`);

ALTER TABLE `강사` ADD FOREIGN KEY (`학군ID`) REFERENCES `학군` (`학군ID`);

ALTER TABLE `가구` ADD FOREIGN KEY (`법정동코드`) REFERENCES `지역` (`법정동코드`);

ALTER TABLE `부동산` ADD FOREIGN KEY (`법정동코드`) REFERENCES `지역` (`법정동코드`);

ALTER TABLE `학군` ADD FOREIGN KEY (`학군ID`) REFERENCES `교육청` (`학군ID`);

ALTER TABLE `유초등학교` ADD FOREIGN KEY (`학군ID`) REFERENCES `학군` (`학군ID`);

ALTER TABLE `중학교` ADD FOREIGN KEY (`학군ID`) REFERENCES `학군` (`학군ID`);

ALTER TABLE `고등학교` ADD FOREIGN KEY (`학군ID`) REFERENCES `학군` (`학군ID`);
