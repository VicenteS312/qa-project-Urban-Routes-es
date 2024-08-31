Vicente Salinas / Sprint 8 / Cohorte 12
# Diseño de pruebas automatizadas para Urban.Routes
### *Descripción del proyecto*
Un importante aspecto de este proyecto fue el aprendizaje de lo que es el 
modelo POM (Page Object Model). Bajo el modelo de POM, las paginas web se 
convierten en clases, los elementos de la pagina web en atributos y la 
interracción con esos atributos en metodos. Utilizar este patrón de diseño 
permite automatizar las pruebas de manera mas concisa. Urban.Routes es una 
aplicación web que facilita servicios de transporte. Se probaron varios 
aspectos de su funionalidad tales como elegir una tarrifa especifica, ingresar
un metodo de pago y dejar un mensaje para el conductor, entre otras. La pagina 
web de Urban.Routes se declaro como una CLASS de acuerdo al POM. Sus elementos
se convirtieron en atributos al asignarles un localizador. Se utilizaron 
varias formas de localizadores pero principalmente CSS_SELECTORS y XPATHS. 
Para interactuar con esos elementos, se declararon metodos que permiten llenar
campos y pulsar botones. Finalmente, con todos estos arreglos hechos en codigo,
se construyeron las pruebas automatizadas con éxito.

### *Descripción de tecnologías y técnicas utilizadas*
> Una tecnología imprescindible para este proyecto fue Selenium WebDriver.
Selenium es un controlador de navegador. Con ella se puede emular las acciones
de un usuario mediante codigo. Se pueden pulsar botones, activar casillas, incluso
cambiar de paginas. Selenium convierte los elementos de una pagina web en atributos
mediante los localizadores de esos elementos. De ahí la importancia de otra 
tecnología essencial para este proyecto: DevTools. Mediante DevTools que 
permite inspeccionar los elementos de la pagina, se pueden extraer los
localizadores particulares de cada elemento necesario para la prueba automatizada.
En cuanto a técnicas implementadas esta el uso de hooks o bloques de codigo 
que establecen precondiciones y limpieza despues de las pruebas. En este 
proyecto se usaron los metodos setup_class() y teardown_class() como ejemplos
de hooks. Con ellos se pudo inicializar el controlador de navegador y cerrarlo 
para todas las pruebas en conjunto en vez de tener que hacerlo para cada prueba 
individual. El uso de esta técnica contribuyo, una vez mas, a un codigo mas
sencillo y facil de manejar. 

### _Instrucciones para ejecutar pruebas_
> 1. Crear archivos: data, main, helpers, UrbanRoutesPage
> 2. Crear variables para los datos necesarios en el archivo data.py
> 3. Dentro del archivo helpers.py crear el metodo de apoyo para recuperar el codigo sms
> 4. En el archivo UrbanRoutesPage.py importar el archivo data.py, helpers.py, entre otros y definir la clase UrbanRoutesPage 
> 5. Define dentro de la clase UrbanRoutesPage los localizadores para los elementos
de la pagina web y crear los metodos para interactuar con esos elementos
> 6. En el archivo main.py armar las funciones que utilizan los metodos del archivo
UrbanRoutesPage.py para hacer las pruebas necesarias
