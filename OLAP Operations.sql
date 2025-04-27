CREATE TABLE SalesData (
    Region VARCHAR(50),
    Product VARCHAR(50),
    Year INT,
    SalesAmount DECIMAL(10, 2)
);

INSERT INTO SalesData (Region, Product, Year, SalesAmount) VALUES
('North', 'Laptop', 2022, 1200.00),
('North', 'Laptop', 2023, 1500.00),
('North', 'Keyboard', 2023, 150.00),
('South', 'Laptop', 2022, 900.00),
('South', 'Keyboard', 2022, 100.00),
('South', 'Keyboard', 2023, 120.00),
('West', 'Laptop', 2023, 1800.00),
('West', 'Monitor', 2023, 400.00);

-- Standard GROUP BY Operation
SELECT
    Region,
    Product,
    SUM(SalesAmount) AS TotalSales
FROM
    SalesData
GROUP BY
    Region,
    Product
ORDER BY
    Region, Product;


-- ROLLUP Operation
SELECT
    Region,
    Product,
    SUM(SalesAmount) AS TotalSales
FROM
    SalesData
GROUP BY
    Region,
    Product
WITH ROLLUP;


-- CUBE Operation (Emulated using UNION ALL as MySQL lacks native CUBE)
SELECT Region, Product, SUM(SalesAmount) AS TotalSales FROM SalesData GROUP BY Region, Product
UNION ALL
SELECT Region, NULL, SUM(SalesAmount) AS TotalSales FROM SalesData GROUP BY Region
UNION ALL
SELECT NULL, Product, SUM(SalesAmount) AS TotalSales FROM SalesData GROUP BY Product
UNION ALL
SELECT NULL, NULL, SUM(SalesAmount) AS TotalSales FROM SalesData
ORDER BY Region IS NULL, Region, Product IS NULL, Product; -- Optional ordering


-- GROUPING SETS Operation
SELECT
    Region,
    Product,
    Year,
    SUM(SalesAmount) AS TotalSales
FROM
    SalesData
GROUP BY
    GROUPING SETS (
        (Region, Product),
        (Region, Year),
        (Product),
        () -- Grand Total
    )
ORDER BY
    Region IS NULL, Region, Product IS NULL, Product, Year IS NULL, Year;
