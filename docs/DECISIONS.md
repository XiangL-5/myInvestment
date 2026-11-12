# Registro de Decisiones de Arquitectura (ADR)

## ADR-001: Desacoplamiento del n�cleo financiero para evoluci�n multiplataforma

### Estado
Aceptado

### Contexto
El sistema debe funcionar de forma 100% local y offline. El objetivo prioritario es entregar un MVP 
en Windows antes de abril de 2027 desarrollado en Python, con la intenci�n posterior de extender 
la interfaz a dispositivos m�viles (Android) mediante Flutter.

### Decisi�n
Implementar Clean Architecture aislando el Dominio y los Casos de Uso en un paquete de Python puro, 
sin frameworks de interfaz ni bases de datos acopladas, comunic�ndose �nicamente mediante DTOs planos.

### Consecuencias
* Permite verificar el 100% de la l�gica contable (FIFO, CMP) mediante tests unitarios r�pidos.
* La interfaz gr�fica de Windows y la futura app m�vil en Flutter consumir�n la misma l�gica sin duplicar c�digo.

ADR-002 (Nuevo): Adopción de modelo único de Cuenta por Propósito (Account) con restricción de nombre único por sesión, descartando tipologías múltiples de custodia física (BROKER, BANK, WALLET).

ADR-003 (Nuevo): Modelado polimórfico de Asset con clase base (id, name, asset_type, currency, description) y subclases especializadas (StockAsset, EtfAsset, MutualFundAsset, CryptoAsset) para garantizar la validez semántica de ticker, isin y network_or_contract.