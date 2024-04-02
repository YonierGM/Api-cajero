Las operaciones a realizar serán:

Eliminación de un banco:
Se podrá eliminar un banco, siempre y cuando:
-el banco si exista.
-no tenga cuentas.

Creación de una cuenta:
Se podrá crear una cuenta nueva en un banco, siempre y cuando:
-el banco aun exista.
-si es de ahorros que el usuario no tenga una cuenta ya de ahorros creada en ese o en otro banco.
-la cuenta no exista a nombre de otra persona, si existe a nombre de la misma persona informar al usuario que ya tiene una, su saldo y hace cuanto la creo, en años.
-si la cuenta es corriente que no tenga más de 3 cuentas corrientes en el mismo banco, y nos más de 6 en bancos diferentes.
-tener en cuenta que al crearla esta debe sumar el campo cantidad de cuentas de la tabla banco al que pertenece.

Eliminación de una cuenta:
Se podrá eliminar una cuenta, siempre y cuando:
-el banco aun exista.
-la cuenta no tenga ingresos negativos, o deudas.
-la cuenta no debe tener ningún saldo, en 0 totales.
-si es cuenta corriente, informar al usuario que otras cuentas corrientes tiene o le quedan, con su número de cuenta, saldo y hace cuanto la creo, en años.
 
Deposito en cuenta:
Se podrá hacer un depósito en una cuenta, siempre y cuando:
-el banco y la cuenta existan.
-la cuenta este a nombre de la persona que hace la transacción.
-la cuenta pertenezca al banco.
-la fecha de la transacción debe ser después de la fecha de creación de la cuenta.
-no supere el monto máximo de transacción del banco.
-no sea inferior al monto mínimo de transacción del banco.

Retiro en cuenta:
Se podrá hacer un retiro en la cuenta, siempre y cuando:
-el banco y la cuenta existan.
-la cuenta este a nombre de la persona que hace la transacción.
-la cuenta pertenezca al banco.
-la fecha de la transacción debe ser después de la fecha de creación de la cuenta.
-no supere el monto máximo de transacción del banco.
-no sea inferior al monto mínimo de transacción del banco.
-haya saldo en la cuenta.
-validar que al momento de la transacción el saldo no quede inferior a $100.000, contando los intereses al año desde que se creó la cuenta y el valor de cobro por transacción, es decir, el saldo restante en la cuenta debe quedar en $100.000 libres de los valores mencionados anteriormente.
