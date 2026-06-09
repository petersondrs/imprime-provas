import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT

def criar_simulados_pdf(nome_arquivo):
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo_style = ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=14, spaceAfter=13, alignment=TA_LEFT)
    subtitulo_style = ParagraphStyle(name='Subtitulo', fontName='Helvetica-Bold', fontSize=12, spaceAfter=8, spaceBefore=10)
    pergunta_style = ParagraphStyle(name='Pergunta', fontName='Helvetica-Bold', fontSize=10, spaceAfter=5, spaceBefore=10, alignment=TA_JUSTIFY)
    opcao_style = ParagraphStyle(name='Opcao', fontName='Helvetica', fontSize=10, leftIndent=15, spaceAfter=3)
    gabarito_style = ParagraphStyle(name='Gabarito', fontName='Helvetica', fontSize=10, spaceAfter=5, alignment=TA_JUSTIFY)

    story = []
    
    # BANCO DE DADOS DAS QUESTÕES
    simulados = [
        {
            "titulo": "SIMULADO 1: Descobrindo a Terra e a Água",
            "multiplas": [
                {
                    "q": "1. Maria assistiu a um documentário e descobriu que nós vivemos na camada mais fina e superficial do planeta. Qual é o nome dessa camada?",
                    "o": ["A) Manto.", "B) Núcleo externo.", "C) Crosta terrestre.", "D) Núcleo interno."],
                    "r": "C", "c": "A crosta terrestre é a camada sólida e externa onde vivemos."
                },
                {
                    "q": "2. Ao analisar um mapa-múndi, João percebeu que um dos oceanos banha a costa leste do Brasil. Que oceano é esse?",
                    "o": ["A) Oceano Índico.", "B) Oceano Pacífico.", "C) Oceano Atlântico.", "D) Oceano Glacial Ártico."],
                    "r": "C", "c": "O Oceano Atlântico é o que banha o litoral brasileiro."
                },
                {
                    "q": "3. O professor mostrou uma rocha escura chamada basalto, que se formou pelo resfriamento da lava de um vulcão. Essa rocha é classificada como:",
                    "o": ["A) Sedimentar.", "B) Magmática (ou Ígnea).", "C) Metamórfica.", "D) Arenosa."],
                    "r": "B", "c": "Rochas magmáticas se formam pelo resfriamento do magma/lava."
                },
                {
                    "q": "4. Durante um passeio no campo, Lucas encontrou o local exato onde um riacho brotava da terra. Como chamamos o lugar onde um rio nasce?",
                    "o": ["A) Foz.", "B) Leito.", "C) Margem.", "D) Nascente."],
                    "r": "D", "c": "A nascente é o ponto onde a água subterrânea aflora, criando o rio."
                },
                {
                    "q": "5. O calor do Sol faz com que a água dos rios e oceanos vire vapor e suba para formar as nuvens. Essa etapa do ciclo da água é a:",
                    "o": ["A) Infiltração.", "B) Evaporação.", "C) Precipitação.", "D) Transpiração."],
                    "r": "B", "c": "A evaporação é a passagem da água do estado líquido para o gasoso."
                },
                {
                    "q": "6. Nas áreas desérticas, as rochas racham por causa do forte calor de dia e do frio à noite. Esse processo de quebra da rocha é o:",
                    "o": ["A) Intemperismo físico.", "B) Intemperismo biológico.", "C) Vulcanismo.", "D) Tectonismo."],
                    "r": "A", "c": "A quebra mecânica por variação de temperatura é intemperismo físico."
                },
                {
                    "q": "7. A maior parte da água doce do planeta que não está congelada encontra-se escondida debaixo dos nossos pés, formando os:",
                    "o": ["A) Mares.", "B) Oceanos.", "C) Aquíferos (águas subterrâneas).", "D) Lagos salgados."],
                    "r": "C", "c": "Os aquíferos guardam a maior reserva de água doce líquida."
                },
                {
                    "q": "8. A chuva forte lavou a terra de um morro sem vegetação, carregando o solo ladeira abaixo. Esse transporte de material é chamado de:",
                    "o": ["A) Magmatismo.", "B) Erosão.", "C) Evaporação.", "D) Condensação."],
                    "r": "B", "c": "Erosão é o desgaste e transporte do solo ou rocha por agentes como a água."
                },
                {
                    "q": "9. A Terra é chamada de Planeta Azul porque tem muita água. Da água total do planeta, a água salgada representa aproximadamente:",
                    "o": ["A) 50%.", "B) 70%.", "C) 2%.", "D) 97%."],
                    "r": "D", "c": "Cerca de 97% de toda a água do mundo é salgada e está nos oceanos."
                },
                {
                    "q": "10. Quando uma rocha é esmagada no fundo da terra, sofrendo muita pressão e calor sem derreter, ela se transforma em uma rocha:",
                    "o": ["A) Magmática.", "B) Metamórfica.", "C) Sedimentar.", "D) Extrusiva."],
                    "r": "B", "c": "Rochas metamórficas surgem da transformação de outras rochas sob calor e pressão."
                },
                {
                    "q": "11. O rio Amazonas deságua no Oceano Atlântico. O lugar onde um rio despeja suas águas no mar é chamado de:",
                    "o": ["A) Nascente.", "B) Aquífero.", "C) Foz.", "D) Afluente."],
                    "r": "C", "c": "A foz é o final do rio, onde ele encontra o mar ou outro rio."
                },
                {
                    "q": "12. Qual é a camada mais profunda, quente e central do planeta Terra?",
                    "o": ["A) Núcleo.", "B) Manto.", "C) Crosta continental.", "D) Crosta oceânica."],
                    "r": "A", "c": "O núcleo é o centro superaquecido da Terra."
                },
                {
                    "q": "13. Na praia, as crianças adoram pular a água que se levanta e quebra na areia, formada principalmente pela força do vento. Estamos falando das:",
                    "o": ["A) Correntes marítimas.", "B) Ondas.", "C) Marés.", "D) Bacias hidrográficas."],
                    "r": "B", "c": "Ondas são oscilações na superfície do mar geradas pelo vento."
                },
                {
                    "q": "14. Restos de conchas, areia e lama se acumularam no fundo do mar por milhares de anos, virando pedra. Que tipo de rocha é essa?",
                    "o": ["A) Metamórfica.", "B) Magmática.", "C) Cristalina.", "D) Sedimentar."],
                    "r": "D", "c": "Rochas sedimentares formam-se pelo acúmulo de sedimentos ao longo do tempo."
                },
                {
                    "q": "15. Quando as nuvens ficam muito pesadas e cheias de gotículas de água, ocorre a chuva. No ciclo da água, a chuva recebe o nome de:",
                    "o": ["A) Infiltração.", "B) Condensação.", "C) Precipitação.", "D) Transpiração."],
                    "r": "C", "c": "Precipitação é o retorno da água à superfície em forma de chuva, neve ou granizo."
                }
            ],
            "discursivas": [
                {
                    "q": "16. Com suas palavras, explique qual é a diferença entre intemperismo e erosão.",
                    "r": "Intemperismo é o desgaste e a quebra da rocha (físico, químico ou biológico). Erosão é o transporte e a remoção desses pedaços de rocha e solo para outro lugar."
                },
                {
                    "q": "17. Por que a Terra é conhecida como 'Planeta Azul' se nós vivemos em terras firmes?",
                    "r": "Porque a maior parte da superfície da Terra (cerca de 71%) é coberta por água, principalmente pelos oceanos, o que dá a cor azul quando vista do espaço."
                },
                {
                    "q": "18. O que são as placas tectônicas e onde elas se localizam?",
                    "r": "São gigantescos blocos sólidos que formam a crosta terrestre e flutuam sobre o manto, movimentando-se lentamente."
                },
                {
                    "q": "19. Defina o que é uma bacia hidrográfica.",
                    "r": "É a área de terras onde a água da chuva escorre para um rio principal e seus afluentes."
                },
                {
                    "q": "20. Como se formam as rochas magmáticas? Dê um exemplo.",
                    "r": "Elas se formam a partir do resfriamento e solidificação do magma (ou lava). Exemplos: basalto e granito."
                }
            ]
        },
        {
            "titulo": "SIMULADO 2: Forças da Natureza e os Oceanos",
            "multiplas": [
                {
                    "q": "1. Pedrinho estava assistindo ao noticiário e viu que a crosta terrestre é dividida em blocos que se movem, causando tremores. Esses blocos são as:",
                    "o": ["A) Bacias oceânicas.", "B) Placas tectônicas.", "C) Rochas sedimentares.", "D) Bacias hidrográficas."],
                    "r": "B", "c": "As placas tectônicas são os blocos da crosta que causam abalos ao se movimentarem."
                },
                {
                    "q": "2. O maior oceano do planeta banha a costa oeste da América do Sul e a costa leste da Ásia. Esse oceano é o:",
                    "o": ["A) Índico.", "B) Atlântico.", "C) Glacial Antártico.", "D) Pacífico."],
                    "r": "D", "c": "O Pacífico é o maior oceano do mundo."
                },
                {
                    "q": "3. Existem agentes que constroem o relevo (internos) e agentes que desgastam o relevo (externos). Assinale um exemplo de agente INTERNO.",
                    "o": ["A) Vento.", "B) Chuva.", "C) Vulcanismo.", "D) Rio."],
                    "r": "C", "c": "Vulcões e terremotos vêm do interior da Terra e constroem/alteram o relevo de dentro para fora."
                },
                {
                    "q": "4. O caminho que um rio percorre da nascente até a foz é chamado de:",
                    "o": ["A) Leito.", "B) Afluente.", "C) Bacia.", "D) Aquífero."],
                    "r": "A", "c": "O leito é o canal por onde as águas do rio correm."
                },
                {
                    "q": "5. O calcário é uma pedra muito comum em cavernas, formada por restos de animais marinhos e conchas antigas. Ele é uma rocha:",
                    "o": ["A) Ígnea.", "B) Metamórfica.", "C) Sedimentar.", "D) Magmática extrusiva."],
                    "r": "C", "c": "O calcário se forma pela união de sedimentos orgânicos (conchas, esqueletos)."
                },
                {
                    "q": "6. Como se chama o movimento de subida e descida das águas do mar que acontece duas vezes por dia por causa da atração da Lua?",
                    "o": ["A) Ondas.", "B) Marés.", "C) Correntes marítimas.", "D) Tsunami."],
                    "r": "B", "c": "As marés são causadas pela atração gravitacional da Lua e do Sol."
                },
                {
                    "q": "7. O Manto da Terra é feito de um material pastoso e muito quente que às vezes escapa por vulcões. Como se chama esse material?",
                    "o": ["A) Granito.", "B) Mármore.", "C) Magma.", "D) Calcário."],
                    "r": "C", "c": "O magma é a rocha derretida que fica no manto."
                },
                {
                    "q": "8. Juliana aprendeu que, no ciclo da água, o vapor sobe, esfria e forma as nuvens. Como se chama essa transformação do gás para o líquido?",
                    "o": ["A) Condensação.", "B) Evaporação.", "C) Infiltração.", "D) Transpiração."],
                    "r": "A", "c": "A condensação é o vapor de água esfriando e virando gotas (nuvens)."
                },
                {
                    "q": "9. A crosta terrestre tem grandes elevações e áreas rebaixadas. Como chamamos uma área rebaixada em relação às áreas ao seu redor?",
                    "o": ["A) Montanha.", "B) Depressão.", "C) Planalto.", "D) Planície."],
                    "r": "B", "c": "Depressão é uma forma de relevo mais baixa que seu entorno."
                },
                {
                    "q": "10. Os rios menores que jogam suas águas em um rio maior e principal recebem o nome de:",
                    "o": ["A) Foz.", "B) Aquíferos.", "C) Afluentes.", "D) Nascentes."],
                    "r": "C", "c": "Afluentes (ou tributários) são rios que deságuam em outro rio."
                },
                {
                    "q": "11. Quando uma rocha é desgastada por seres vivos, como raízes de árvores quebrando pedras, chamamos isso de:",
                    "o": ["A) Intemperismo físico.", "B) Intemperismo químico.", "C) Intemperismo biológico.", "D) Erosão eólica."],
                    "r": "C", "c": "Intemperismo biológico é a ação de plantas e animais quebrando rochas."
                },
                {
                    "q": "12. Qual oceano fica entre a África, a Ásia e a Oceania, sendo o terceiro maior do mundo?",
                    "o": ["A) Atlântico.", "B) Pacífico.", "C) Ártico.", "D) Índico."],
                    "r": "A", "c": "O Oceano Índico fica nessa posição geográfica exata."
                },
                {
                    "q": "13. Algumas águas da chuva não escorrem, mas entram na terra e alimentam os lençóis freáticos. O nome desse processo é:",
                    "o": ["A) Condensação.", "B) Evaporação.", "C) Infiltração.", "D) Transpiração."],
                    "r": "C", "c": "A infiltração é a água penetrando no solo."
                },
                {
                    "q": "14. As gigantescas cadeias de montanhas, como os Andes e o Himalaia, formaram-se devido:",
                    "o": ["A) Ao vento constante.", "B) Ao choque entre placas tectônicas.", "C) À chuva forte.", "D) Ao congelamento do solo."],
                    "r": "B", "c": "O dobramento provocado pelo choque das placas cria montanhas."
                },
                {
                    "q": "15. A maior porção de água doce do mundo é de difícil acesso porque está na forma de:",
                    "o": ["A) Gelo nas geleiras e calotas polares.", "B) Água dos rios poluídos.", "C) Vapor na atmosfera.", "D) Água no corpo humano."],
                    "r": "A", "c": "As calotas polares e geleiras guardam cerca de 68% da água doce do mundo."
                }
            ],
            "discursivas": [
                {
                    "q": "16. Cite os três tipos principais de rochas e explique um deles.",
                    "r": "Magmáticas, sedimentares e metamórficas. Magmáticas formam-se do resfriamento do magma. (Pode explicar qualquer um)."
                },
                {
                    "q": "17. Como acontece a maré alta e a maré baixa?",
                    "r": "Acontecem pela força de atração gravitacional que a Lua e o Sol exercem sobre as águas dos oceanos na Terra."
                },
                {
                    "q": "18. Explique o que é a infiltração no ciclo da água e qual a sua importância.",
                    "r": "É quando a água da chuva entra no solo. É importante porque forma as reservas subterrâneas (aquíferos) que abastecem plantas e rios."
                },
                {
                    "q": "19. O que são os agentes externos do relevo? Dê dois exemplos.",
                    "r": "São os elementos que desgastam e modelam o relevo na superfície. Exemplos: vento, chuva, rios, gelo."
                },
                {
                    "q": "20. Se 97% da água do mundo é salgada, onde encontramos os 3% de água doce?",
                    "r": "Nas geleiras, águas subterrâneas (aquíferos), rios, lagos e na atmosfera."
                }
            ]
        },
        {
            "titulo": "SIMULADO 3: Moldando a Paisagem e os Rios",
            "multiplas": [
                {
                    "q": "1. As estalactites nas cavernas são rochas formadas ao longo de milhares de anos por minerais carregados pela água. Elas são rochas:",
                    "o": ["A) Magmáticas.", "B) Sedimentares.", "C) Metamórficas.", "D) Ígneas."],
                    "r": "B", "c": "Elas se formam por deposição química de minerais (sedimentar química)."
                },
                {
                    "q": "2. O vento carrega a areia e bate nas pedras, esculpindo-as com o tempo. Isso é um tipo de desgaste causado por um agente:",
                    "o": ["A) Interno.", "B) Externo.", "C) Subterrâneo.", "D) Magmático."],
                    "r": "B", "c": "O vento é um agente externo que atua modelando o relevo."
                },
                {
                    "q": "3. O rio São Francisco é o maior do Brasil em volume de água. As partes de terra que ficam nas laterais do rio são chamadas de:",
                    "o": ["A) Nascente.", "B) Foz.", "C) Margens.", "D) Leito."],
                    "r": "C", "c": "Margens são as terras que delimitam o rio pelas laterais."
                },
                {
                    "q": "4. Carlos viu na escola que a temperatura da Terra aumenta conforme vamos mais fundo. A camada intermediária entre a crosta e o núcleo é o:",
                    "o": ["A) Núcleo externo.", "B) Manto.", "C) Litosfera.", "D) Biosfera."],
                    "r": "B", "c": "O manto fica logo abaixo da crosta e envolve o núcleo."
                },
                {
                    "q": "5. O mármore, muito usado em pias, era originalmente uma rocha de calcário que foi submetida a muito calor e pressão na Terra. O mármore é uma rocha:",
                    "o": ["A) Sedimentar.", "B) Magmática.", "C) Metamórfica.", "D) Extrusiva."],
                    "r": "C", "c": "Por ter sofrido transformação por pressão e calor, é metamórfica."
                },
                {
                    "q": "6. A água dos oceanos se movimenta como 'rios' gigantes dentro do mar, levando águas quentes ou frias pelo planeta. São as:",
                    "o": ["A) Ondas de superfície.", "B) Correntes marítimas.", "C) Marés mortas.", "D) Bacias marinhas."],
                    "r": "B", "c": "As correntes marítimas são grandes fluxos de água circulando nos oceanos."
                },
                {
                    "q": "7. As áreas mais planas e baixas do relevo, frequentemente formadas pelo acúmulo de terra e areia trazidas por rios, são as:",
                    "o": ["A) Montanhas.", "B) Depressões.", "C) Planícies.", "D) Cordilheiras."],
                    "r": "C", "c": "Planícies são relevos baixos onde predomina o depósito de sedimentos."
                },
                {
                    "q": "8. Em locais muito úmidos e com muita chuva, as pedras vão 'enferrujando' e se desfazendo pela reação com a água. Esse é o intemperismo:",
                    "o": ["A) Físico.", "B) Químico.", "C) Biológico.", "D) Magmático."],
                    "r": "B", "c": "A alteração química causada pela água caracteriza o intemperismo químico."
                },
                {
                    "q": "9. No ciclo da água, além da evaporação dos rios, as plantas também perdem água para o ar. Esse processo chama-se:",
                    "o": ["A) Precipitação.", "B) Condensação.", "C) Transpiração.", "D) Escoamento."],
                    "r": "C", "c": "As plantas liberam vapor de água pela transpiração."
                },
                {
                    "q": "10. Quando duas placas tectônicas se chocam violentamente sob o mar, pode ocorrer um imenso deslocamento de água, gerando um:",
                    "o": ["A) Furacão.", "B) Ciclone.", "C) Tsunami.", "D) Aquífero."],
                    "r": "C", "c": "Tsunamis são ondas gigantes geradas por tremores no fundo do oceano."
                },
                {
                    "q": "11. Um relevo com altitudes elevadas, superfícies acidentadas e que sofre mais desgaste (erosão) do que recebe materiais (sedimentos) é o:",
                    "o": ["A) Planalto.", "B) Planície.", "C) Foz.", "D) Leito."],
                    "r": "A", "c": "Os planaltos são terrenos geralmente mais altos onde a erosão é mais forte que a sedimentação."
                },
                {
                    "q": "12. Qual é o nome do aquífero gigante que se espalha por grande parte da América do Sul, incluindo vários estados brasileiros?",
                    "o": ["A) Aquífero Amazonas.", "B) Aquífero Guarani.", "C) Aquífero São Francisco.", "D) Aquífero Tectônico."],
                    "r": "B", "c": "O Aquífero Guarani é um dos maiores do mundo e pega boa parte do Brasil."
                },
                {
                    "q": "13. O que acontece com a água durante a etapa de evaporação do ciclo hidrológico?",
                    "o": ["A) Ela vira gelo.", "B) Ela entra na terra.", "C) Ela vira gás e sobe para o ar.", "D) Ela cai como chuva."],
                    "r": "C", "c": "O vapor sobe para a atmosfera."
                },
                {
                    "q": "14. Ao fazer um poço no quintal, Tiago encontrou água muito limpa nas profundezas. Essa água pertence a um:",
                    "o": ["A) Afluente.", "B) Oceano.", "C) Lençol freático (águas subterrâneas).", "D) Rio principal."],
                    "r": "C", "c": "Lençóis freáticos são reservatórios de água no subsolo."
                },
                {
                    "q": "15. A parte da Geografia que estuda a formação e classificação do chão que pisamos (rochas e solo) faz parte da:",
                    "o": ["A) Geologia.", "B) Hidrografia.", "C) Meteorologia.", "D) Astronomia."],
                    "r": "A", "c": "Geologia é a ciência que estuda a terra, rochas e sua estrutura."
                }
            ],
            "discursivas": [
                {
                    "q": "16. Cite os quatro tipos principais de relevo continental.",
                    "r": "Montanhas, planaltos, planícies e depressões."
                },
                {
                    "q": "17. O que é o intemperismo químico e onde ele acontece com mais frequência?",
                    "r": "É a quebra e alteração das rochas por reações com a água. Acontece mais em climas úmidos e quentes."
                },
                {
                    "q": "18. Explique por que os oceanos são importantes para a vida na Terra, mesmo sendo salgados.",
                    "r": "Eles ajudam a regular a temperatura do planeta, abrigam muita vida marinha e fornecem grande parte do vapor para o ciclo da água."
                },
                {
                    "q": "19. Descreva as partes principais de um rio.",
                    "r": "Nascente (onde nasce), leito (caminho), margens (laterais) e foz (onde deságua)."
                },
                {
                    "q": "20. O que as plantas têm a ver com o ciclo da água?",
                    "r": "As plantas absorvem água do solo e a devolvem para o ar na forma de vapor, por meio da transpiração."
                }
            ]
        },
        {
            "titulo": "SIMULADO 4: A Dinâmica da Água e da Terra",
            "multiplas": [
                {
                    "q": "1. O Brasil quase não sofre com grandes terremotos e vulcões porque:",
                    "o": ["A) Nosso clima é muito quente.", "B) Estamos no centro de uma placa tectônica (Placa Sul-Americana).", "C) Temos muitos aquíferos.", "D) Não temos montanhas altas."],
                    "r": "B", "c": "Estar no centro da placa nos afasta das bordas, onde ocorrem os choques."
                },
                {
                    "q": "2. No passeio da escola, Sofia viu que o rio principal recebia águas de rios menores ao longo do caminho. Todo esse conjunto de terras banhadas por eles forma uma:",
                    "o": ["A) Bacia hidrográfica.", "B) Placa tectônica.", "C) Planície de gelo.", "D) Rocha sedimentar."],
                    "r": "A", "c": "Bacia hidrográfica é a área drenada por um rio e seus afluentes."
                },
                {
                    "q": "3. O granito, pedra muito comum no piso e bancadas de cozinha, é uma rocha forte formada pelo lento resfriamento do magma dentro da crosta. O granito é uma rocha:",
                    "o": ["A) Sedimentar clástica.", "B) Magmática intrusiva.", "C) Metamórfica orgânica.", "D) Vulcânica de superfície."],
                    "r": "B", "c": "É magmática por vir do magma e intrusiva por esfriar dentro da terra."
                },
                {
                    "q": "4. Muitas vezes as marés sobem muito (maré alta) ou descem bastante (maré baixa). Quantas vezes, em média, vemos a maré alta ocorrer em um dia na praia?",
                    "o": ["A) Uma vez.", "B) Duas vezes.", "C) Quatro vezes.", "D) Dez vezes."],
                    "r": "B", "c": "Geralmente temos duas marés altas e duas baixas por dia (a cada ~6 horas)."
                },
                {
                    "q": "5. Quando dizemos que a água da chuva escorreu pela superfície da terra e foi parar no rio, estamos falando de:",
                    "o": ["A) Escoamento superficial.", "B) Infiltração profunda.", "C) Evapotranspiração.", "D) Condensação gasosa."],
                    "r": "A", "c": "Escoamento superficial é a água que corre por cima do solo."
                },
                {
                    "q": "6. Qual foi o estado físico da água predominante que esculpiu os vales em formato de 'U' conhecidos como fiordes no passado da Terra?",
                    "o": ["A) Gasoso.", "B) Líquido.", "C) Sólido (Geleiras).", "D) Vapor quente."],
                    "r": "C", "c": "O atrito do gelo (sólido) das antigas geleiras esculpiu grandes rochas."
                },
                {
                    "q": "7. O petróleo e o carvão mineral (combustíveis fósseis) são encontrados armazenados em qual tipo de rocha que se acumulou ao longo de milhões de anos?",
                    "o": ["A) Ígneas.", "B) Metamórficas.", "C) Vulcânicas.", "D) Sedimentares."],
                    "r": "D", "c": "O soterramento orgânico em rochas sedimentares cria combustíveis fósseis."
                },
                {
                    "q": "8. Ao olharmos um globo terrestre, vemos muito mais cor azul do que cor marrom ou verde. Isso ocorre porque:",
                    "o": ["A) Os mares são rasos.", "B) As nuvens azuis cobrem a Terra.", "C) Cerca de 71% do planeta é coberto por oceanos.", "D) O gelo do polo sul é infinito."],
                    "r": "C", "c": "A grande extensão dos oceanos justifica a cor azul."
                },
                {
                    "q": "9. As cordilheiras modernas, cheias de montanhas pontiagudas como o Himalaia, surgiram devido a qual agente interno?",
                    "o": ["A) Vento que sopra no topo.", "B) Chuvas que levam areia.", "C) Tectonismo (movimento das placas).", "D) Água de lagos."],
                    "r": "C", "c": "A força tectônica ergue enormes blocos de terra (orogênese)."
                },
                {
                    "q": "10. Um rio nunca seca completamente, mesmo se ficar um tempo sem chover. Ele continua fluindo porque é alimentado gradualmente por:",
                    "o": ["A) Águas subterrâneas (lençóis freáticos).", "B) Oceanos vizinhos.", "C) Gelo de marés.", "D) Evaporação instantânea."],
                    "r": "A", "c": "As águas subterrâneas minam no leito do rio garantindo seu fluxo contínuo."
                },
                {
                    "q": "11. O desgaste nas calçadas antigas e pedras expostas ao clima da cidade é um exemplo lento, mas visível, de:",
                    "o": ["A) Terremoto.", "B) Tsunami.", "C) Intemperismo.", "D) Magmatismo."],
                    "r": "C", "c": "O sol, chuva e vento desgastam materiais lentamente pelo intemperismo."
                },
                {
                    "q": "12. Qual oceano banha as águas frias da Antártida no polo sul do nosso planeta Azul?",
                    "o": ["A) Oceano Atlântico Norte.", "B) Oceano Glacial Antártico.", "C) Oceano Glacial Ártico.", "D) Oceano Índico Tropical."],
                    "r": "B", "c": "O Oceano Glacial Antártico circunda o continente gelado da Antártida no sul."
                },
                {
                    "q": "13. O que podemos fazer para ajudar a proteger os rios da erosão pesada de suas margens?",
                    "o": ["A) Plantar árvores nas margens (mata ciliar).", "B) Retirar todas as raízes.", "C) Jogar pedras grandes soltas.", "D) Colocar fogo no mato."],
                    "r": "A", "c": "A vegetação ciliar segura a terra com as raízes, evitando a erosão."
                },
                {
                    "q": "14. Uma depressão relativa é:",
                    "o": ["A) Uma montanha muito alta.", "B) Uma área mais baixa que as terras em volta, mas acima do nível do mar.", "C) O fundo do oceano.", "D) Um vulcão deitado."],
                    "r": "B", "c": "Depressão relativa é rebaixada, mas fica acima do nível do mar (diferente da absoluta)."
                },
                {
                    "q": "15. No ciclo hidrológico contínuo, a água NUNCA desaparece, ela apenas:",
                    "o": ["A) Flutua para o espaço.", "B) É consumida pelos peixes para sempre.", "C) Muda de estado físico e de localização.", "D) Queima no núcleo da Terra."],
                    "r": "C", "c": "A água não acaba, ela é renovada através do seu ciclo mudando de vapor para água e gelo."
                }
            ],
            "discursivas": [
                {
                    "q": "16. Por que o Brasil praticamente não sofre com terremotos e tsunamis fortes?",
                    "r": "Porque o Brasil está bem no centro de uma placa tectônica (Placa Sul-Americana), longe das bordas onde ocorrem os grandes choques de placas."
                },
                {
                    "q": "17. O que são os aquíferos e por que eles são importantes para a sociedade?",
                    "r": "São reservatórios gigantes de água doce debaixo da terra. São importantes porque abastecem os rios e servem de água limpa para consumo humano em várias cidades."
                },
                {
                    "q": "18. Explique como o intemperismo físico age sobre as rochas nos desertos.",
                    "r": "De dia faz muito calor e a rocha incha. De noite faz frio e a rocha encolhe. Esse movimento repetitivo faz a pedra quebrar."
                },
                {
                    "q": "19. O que é uma rocha sedimentar? Explique como ela se forma.",
                    "r": "É uma rocha formada pelo acúmulo e cimentação de pequenas partículas (sedimentos) de areia, barro ou restos de animais no fundo de lagos e mares ao longo de milhões de anos."
                },
                {
                    "q": "20. O que significa dizer que as águas na Terra formam um 'ciclo'?",
                    "r": "Significa que a água está em movimento infinito: evapora pelo Sol, condensa nas nuvens, cai como chuva, escorre para os rios, entra na terra e o processo recomeça."
                }
            ]
        }
    ]

    # Constroi as páginas do PDF
    for sim in simulados:
        story.append(Paragraph(sim["titulo"], titulo_style))
        story.append(Spacer(1, 10))
        
        # Múltipla Escolha
        story.append(Paragraph("PARTE 1: Múltipla Escolha", subtitulo_style))
        for m in sim["multiplas"]:
            bloco = [Paragraph(m["q"], pergunta_style)]
            for op in m["o"]:
                bloco.append(Paragraph(op, opcao_style))
            bloco.append(Spacer(1, 5))
            story.append(KeepTogether(bloco))
            
        story.append(Spacer(1, 10))
        
        # Discursivas
        story.append(Paragraph("PARTE 2: Questões Discursivas", subtitulo_style))
        for d in sim["discursivas"]:
            bloco = [Paragraph(d["q"], pergunta_style)]
            for _ in range(4):
                bloco.append(HRFlowable(width="100%", thickness=0.5, spaceAfter=15))
            bloco.append(Spacer(1, 10))
            story.append(KeepTogether(bloco))
            
        story.append(PageBreak())

    # GABARITO COMENTADO (NO FINAL, ISOLADO)
    story.append(Paragraph("GABARITO COMENTADO DOS SIMULADOS", titulo_style))
    story.append(PageBreak())

    label_style = ParagraphStyle(name='Bold', fontName='Helvetica-Bold', fontSize=11, spaceAfter=5)
    for i, sim in enumerate(simulados):
        if i > 0:
            story.append(PageBreak())

        bloco = [
            Paragraph(sim["titulo"], subtitulo_style),
            Paragraph("Múltipla Escolha:", label_style),
        ]
        for idx, m in enumerate(sim["multiplas"]):
            gab_text = f"<b>{idx+1}. {m['r']}</b> - {m['c']}"
            bloco.append(Paragraph(gab_text, gabarito_style))

        bloco.append(Spacer(1, 10))
        bloco.append(Paragraph("Discursivas (Expectativa de Resposta):", label_style))

        for d in sim["discursivas"]:
            num = d['q'].split(".")[0]
            gab_text = f"<b>{num}.</b> {d['r']}"
            bloco.append(Paragraph(gab_text, gabarito_style))

        story.append(KeepTogether(bloco))

    doc.build(story)
    print(f"Sucesso! O arquivo '{nome_arquivo}' foi criado com as regras solicitadas.")

# Chama a função para gerar o arquivo
criar_simulados_pdf("Simulados_Geografia_Cap6_e_7.pdf")