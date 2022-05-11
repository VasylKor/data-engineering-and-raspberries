CREATE TABLE `AdjClosedPrices` (
  `Id` int(11) NOT NULL,
  `Datetime` datetime DEFAULT NULL,
  `AAPL` double DEFAULT NULL,
  `GOOG` double DEFAULT NULL,
  `MSFT` double DEFAULT NULL,
  `TSLA` double DEFAULT NULL,
  PRIMARY KEY (`Id`)
)