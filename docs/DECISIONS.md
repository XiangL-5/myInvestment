# Registro de Decisiones de Arquitectura (ADR)

## ADR-001: Desacoplamiento del núcleo financiero para evolución multiplataforma

### Estado
Aceptado

### Contexto
El sistema debe funcionar de forma 100% local y offline. El objetivo prioritario es entregar un MVP 
en Windows antes de abril de 2027 desarrollado en Python, con la intención posterior de extender 
la interfaz a dispositivos móviles (Android) mediante Flutter.

### Decisión
Implementar Clean Architecture aislando el Dominio y los Casos de Uso en un paquete de Python puro, 
sin frameworks de interfaz ni bases de datos acopladas, comunicándose únicamente mediante DTOs planos.

### Consecuencias
* Permite verificar el 100% de la lógica contable (FIFO, CMP) mediante tests unitarios rápidos.
* La interfaz gráfica de Windows y la futura app móvil en Flutter consumirán la misma lógica sin duplicar código.
