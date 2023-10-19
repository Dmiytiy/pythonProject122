WITH ProductCategory_hierarchy AS (
    SELECT pc.Id, 'ProductCategory ' + CAST(pc.Id AS VARCHAR(max)) + ':' + pc.Name AS cat
    FROM ProductCategory pc
    WHERE pc.Parent IS NULL

    UNION ALL

    SELECT pc.Id, ph.cat + '&&ProductCategory ' + CAST(pc.Id AS VARCHAR(max)) + ':' + pc.Name AS cat
    FROM ProductCategory pc
    JOIN ProductCategory_hierarchy ph ON pc.Parent = ph.Id
),
PrevPurchases AS (
    SELECT ls.Period, ls.AccountID,
           LAG(ls.Period) OVER (PARTITION BY ls.AccountID ORDER BY ls.Period) AS prev_period,
           DATEDIFF(DAY, LAG(ls.Period) OVER (PARTITION BY ls.AccountID ORDER BY ls.Period), ls.Period) AS days_since_prev_purchase
    FROM LoyaltyProgramSales ls
    WHERE ls.Amount >= 0
    GROUP BY ls.AccountID, ls.Period
)

SELECT TOP 1 ls.ModifiedDate,
            SUM(ls.Amount) OVER (PARTITION BY s.Code, s1.Code, ls.Period, ls.IDSale) AS amount,
            DATEADD(SECOND, 43200 + CHECKSUM(ls.IDSale) % 43200,
                    DATEADD(DAY, DATEDIFF(DAY, 0, ls.Period), 0)) AS ts,
            0 AS discount,
            ISNULL(e.Name, '') AS cashier,
            LTRIM(RTRIM(ls.IDSale)) AS ext_id,
            CAST(s1.Code AS VARCHAR(max)) + '-' + CAST(s.Code AS VARCHAR(max)) AS store_ext_id,
            pp.prev_period,
            pp.days_since_prev_purchase,
            CASE WHEN (a.StatusLP IN (15, 16)) THEN 1 ELSE 0 END AS is_installer,
            SUM(ls.ProfitZP) OVER (PARTITION BY s.Code, s1.Code, ls.Period, ls.IDSale) AS profit,
            CASE WHEN (ls.Amount >= 0 AND MIN(ls.IDSale) OVER (PARTITION BY ls.AccountID, ls.Period) = ls.IDSale) THEN 1 ELSE 0 END AS is_first_daily_purchase,
            CASE WHEN (ls.Amount >= 0 AND a.AccountDate = ls.Period AND MIN(ls.IDSale) OVER (PARTITION BY ls.AccountID, ls.Period) = ls.IDSale) THEN 1 ELSE 0 END AS is_new_account,
            COALESCE(a.StatusLP, -1) AS status_lp,
            ls.PaymentType,
            p.Name AS name,
            ls.ProductID AS price_ext_id,
            ABS(ls.Quantity) AS count,
            ABS(ls.Amount) AS total,
            pch.cat AS prod_category,
            ls.DocumentLines AS line_count
FROM LoyaltyProgramSales ls
LEFT OUTER JOIN Employee e ON e.Id = ls.EmployeeID
LEFT OUTER JOIN Account a ON a.Id = ls.AccountID
LEFT OUTER JOIN Product p ON p.Id = ls.ProductID
LEFT OUTER JOIN ProductCategory_hierarchy pch ON pch.Id = p.ProductCategory
LEFT OUTER JOIN Store s ON s.Id = ls.StoreID
LEFT OUTER JOIN Store s1 ON s.Parent_1CID = s1.1C_Id
LEFT OUTER JOIN PrevPurchases pp ON pp.AccountID = ls.AccountID AND pp.Period = ls.Period
ORDER BY ls.ModifiedDate, ext_id, store_ext_id;