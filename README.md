Las operaciones a realizar serán:

Eliminación de un banco:
Se podrá eliminar un banco, siempre y cuando: <br > <br >
-el banco si exista. <br >
-no tenga cuentas. <br ><br >

Creación de una cuenta:<br >
Se podrá crear una cuenta nueva en un banco, siempre y cuando: <br ><br >
-el banco aun exista.<br >
-si es de ahorros que el usuario no tenga una cuenta ya de ahorros creada en ese o en otro banco.<br >
-la cuenta no exista a nombre de otra persona, si existe a nombre de la misma persona informar al usuario que ya tiene una, su saldo y hace cuanto la creo, en años.<br >
-si la cuenta es corriente que no tenga más de 3 cuentas corrientes en el mismo banco, y nos más de 6 en bancos diferentes.<br >
-tener en cuenta que al crearla esta debe sumar el campo cantidad de cuentas de la tabla banco al que pertenece.<br >

Eliminación de una cuenta:<br >
Se podrá eliminar una cuenta, siempre y cuando:<br ><br >
-el banco aun exista.<br >
-la cuenta no tenga ingresos negativos, o deudas.<br >
-la cuenta no debe tener ningún saldo, en 0 totales.<br >
-si es cuenta corriente, informar al usuario que otras cuentas corrientes tiene o le quedan, con su número de cuenta, saldo y hace cuanto la creo, en años.<br >
 
Deposito en cuenta:<br >
Se podrá hacer un depósito en una cuenta, siempre y cuando:<br ><br >
-el banco y la cuenta existan.<br >
-la cuenta este a nombre de la persona que hace la transacción.<br >
-la cuenta pertenezca al banco.<br >
-la fecha de la transacción debe ser después de la fecha de creación de la cuenta.<br >
-no supere el monto máximo de transacción del banco.<br >
-no sea inferior al monto mínimo de transacción del banco.<br >

Retiro en cuenta:<br >
Se podrá hacer un retiro en la cuenta, siempre y cuando:<br ><br >
-el banco y la cuenta existan.<br >
-la cuenta este a nombre de la persona que hace la transacción.<br >
-la cuenta pertenezca al banco.<br >
-la fecha de la transacción debe ser después de la fecha de creación de la cuenta.<br >
-no supere el monto máximo de transacción del banco.<br >
-no sea inferior al monto mínimo de transacción del banco.<br >
-haya saldo en la cuenta.<br >
-validar que al momento de la transacción el saldo no quede inferior a $100.000, contando los intereses al año desde que se creó la cuenta y el valor de cobro por transacción, es decir, el saldo restante en la cuenta debe quedar en $100.000 libres de los valores mencionados anteriormente.<br >
