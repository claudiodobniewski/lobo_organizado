__ LOBO ORGANIZADO __

# STAGE

# RELEASE 0.4.0 26/11/2023
* Reportes CSV completo en listados de cuotas cobradas y gestion de cobrana (estado de pago de cuota scocial familias)
* NUEVO ficha familias ahora eXPORT PDF completo, incluye cuenta corriente de la familia con identificador de pago interno y comprobante (MP)
* Se suma al admin de planes de pago de django capors "orden", "plan_default" y "excluir" para su gestion. Actualmente "plan_default" opera sobre el plan preseleccionado al ingresar una cuota nueva, evitando que el default sea un plan de años anteriores. Los demas campos se deben implementar funcionalidad aun.

# RELEASE 0.3.4 12/11/2023
* Fix sobre generacion reportes
* Feature se suma reporte de cuotas a reportes CSV!

# RELEASE 0.3.3 12/11/2023

## ATENCION
* Requiere ejecutar migraciones con _python3 manage.py migrate_
  *  la neueva migracion es lobo_organizado/cuotas/migrations/0030_plandepago_excluir.py
  *  este flag (aun no soportado en codigo) oermitira eliminar de las busquedas planes de pago viejos que ya no se quieran tener en cuenta. 

## NEWS
* fix Cuando no hay resultados en la busqueda, se rompe al querer paginar sobre 0 registros.
* Mejoras listados cobranza y se incluye hash unico para cada cobro (ademas de su PK)
* Listado de cuotas cobradas con comprobante y hash de cuota
* #34 busquedas sin resultados  fixed
* #11 se fixea en varias paginas acceso sin sesion activa en template
* #39 en listado cuotas vencidas, "solo vencidas"
* Feature UX Mejoras experiencia: En detalle cobranza familia detale, boton nuevo pago ARRIBA de la cobranza, junto con el status y el boton de cuenta corriente.
* Feature UX Mejoras experiencia: Seccion cuotas, ahora tiene titulo , y el detalle esta oculto, si se hace click en titulo, se despliega, vision mas limpia
* Feature Con este flag "True" no se van a incluir nada relacionada a dicho plan de palgo (plan de pago, cuotas , cobros) en consultas, pantallas, informes, etc.
Permite generar info mas limpia excluyendo infor relacionada a años muy viejos
* Se inicia soporte para generar una imagen docker y levantar la APP en un container docker.
* Nuevo export: Ahora se puede exportar a CSV ademas de PDF! en lugar del checkbox PDF es un select default NO, opciones PDF y CSV, por ahora solo funciona CSV de estado de deuda familias (gestion de cobranza), la intencion es extenderlo al listado de pagos, y ficha cuenta corriente de familia.


# RELEASE 0.3.2 02/04/2022

# RELEASE 0.3.1 13/03/2022

# RELEASE 0.3.0 12/03/2022

# RELEASE 0.2.0 12/09/2021

# RELEASE 0.1.0 08/07/2021
