select a.orderNumber, a.orderDate, b.customerName, b.city, b.country, c.quantityOrdered, d.productName
from orders a
inner join customers b on a.customerNumber = b.customerNumber
inner join orderdetails c on a.orderNumber = c.orderNumber
inner join products d on c.productCode = d.productCode
where d.productName = '1992 Ferrari 360 Spider red'
and a.orderDate between '2004-08-01' and '2004-12-01'
order by b.country asc
;