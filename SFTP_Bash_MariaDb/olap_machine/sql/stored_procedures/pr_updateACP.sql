CREATE PROCEDURE `finance`.`pr_UpdateACP`()
BEGIN
	INSERT INTO finance.AdjClosedPrices ()
	SELECT 
		Id,
		`Datetime`,
		AAPL ,
		GOOG,
		MSFT,
		TSLA
	FROM stg.AdjClosedPrices 
	ON DUPLICATE KEY UPDATE 
	AAPL = stg.AdjClosedPrices.AAPL,
	GOOG = stg.AdjClosedPrices.GOOG,
	MSFT = stg.AdjClosedPrices.MSFT,
	TSLA = stg.AdjClosedPrices.TSLA;

END