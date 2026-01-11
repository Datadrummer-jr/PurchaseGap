Datapyme es un proyecto de ciencia de datos que analiza cómo las fluctuaciones del dólar estadounidense y otras divisas extranjeras impactan directamente en los precios locales en Cuba. Su propósito central es mostrar cómo estos cambios afectan la capacidad de compra del cubano de a pie, revelando la brecha creciente entre salarios y costos de productos básicos. Al estudiar la dinámica de inflación y la accesibilidad del consumidor, el proyecto busca visibilizar los mecanismos que limitan el acceso a bienes esenciales y explicar por qué la vida cotidiana se vuelve cada vez más difícil para la mayoría de la población.

1- Para analizar los datos se recogieron datos de la fuente que más usado como referencia para saber precio del toque en mercado informal "El Toque". Para ello scrapee obtuve los datos del toque desde incios de año hasta la mitad de diciembre a través de su API usando la biblioteca para python httpx y luego para mostrar datos se utilizó la biblioteca para python plotly para mostrar un gráfico atractivo para apreciar el comportamiento USD, EURO y MLC durante la mayor parte de 2025 como se puede ver a continuación.

![Graph Coin](static_charts/graph_coin.png)

2 - Uno de los efectos en los altos precios del usd y euro en Cuba es en los precios de las mipymes ya que los precios de las mipymes que venden productos en monedas extrajeras tienen precio media superior a las mipymes q venden en mondeda nacional (CUP), por lo que recopilé todods los precios de los productos de las mipymes en cup y los precios de las mipymes q venden en euro y en usd para comparar precio media de ambos grupos.

![Graph Coin](static_charts/coin_pymes.png)

3- Para comparar como se comportan los recios canasta básica vs mipymes obtuve los precios de la canasta básica de la url oficial del MINCIN https://www.mincin.gob.cu/es/faq/cuales-son-los-precios-de-los-productos-de-la-canasta-familiar-normada y para los precios de las mipymes de algunas que visité personalmente y otras que obtuve los precios por medio de scraping usando la herramienta de python playwright por dificultades por el transporte y problemas de salud. Y el resultado de dichas capturas de datos término en un par de gráficas de barras hechas con plotly.

![Graph Pymes vs Cansta Básica](static_charts\canasta_vs_pymes.png)
