import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')  # Usar backend não interativo para salvar sem abrir janela
import matplotlib.pyplot as plt
import os
import sys
import json
import datetime
import random
import string
import atexit
import signal
import platform
import getpass

# =======================================================
# DICIONÁRIO DE TRADUÇÕES
# =======================================================
TRADUCOES = {
    'portugues': {
        'welcome': "Bem-vindo ao analisador de letras!",
        'lang_question': "Escolha o idioma: 1-Português, 2-Inglês, 3-Francês, 4-Espanhol, 5-Árabe, 6-Italiano",
        'lang_invalid': "Idioma inválido. Usando Português.",
        'input_letters': "Digite as letras possíveis separadas por espaço (ex: a b c): ",
        'input_responses': "Digite a sequência de respostas (letras separadas por espaço): ",
        'input_order_question': "Deseja definir a ordem (número 1-7) para cada letra? (s/n): ",
        'input_order_manual': "Digite no formato 'letra:número' (ex: a:1 b:2). Pressione Enter para usar padrão: ",
        'input_period_question': "Deseja configurar os períodos (médias móveis e MACD)? (s/n): ",
        'input_mm_short': "Período da média móvel curta (padrão 2): ",
        'input_mm_long': "Período da média móvel longa (padrão 10): ",
        'input_macd_fast': "Período rápido MACD (padrão 12): ",
        'input_macd_slow': "Período lento MACD (padrão 26): ",
        'input_macd_signal': "Período sinal MACD (padrão 9): ",
        'input_save_dir': "Digite o diretório para salvar os arquivos (ou deixe vazio para padrão): ",
        'input_filename': "Digite o nome base do arquivo (ou deixe vazio para nome aleatório): ",
        'input_save_hist': "Deseja salvar histórico do usuário? (s/n): ",
        'saving': "Salvando resultados...",
        'success': "Análise concluída com sucesso!",
        'output_files': "Arquivos gerados:",
        'error': "Erro: ",
        'goodbye': "Encerrando. Até logo!"
    },
    'ingles': {
        'welcome': "Welcome to letter analyzer!",
        'lang_question': "Choose language: 1-Portuguese, 2-English, 3-French, 4-Spanish, 5-Arabic, 6-Italian",
        'lang_invalid': "Invalid language. Using Portuguese.",
        'input_letters': "Enter possible letters separated by space (e.g., a b c): ",
        'input_responses': "Enter response sequence (letters separated by space): ",
        'input_order_question': "Do you want to define order (number 1-7) for each letter? (y/n): ",
        'input_order_manual': "Enter in format 'letter:number' (e.g., a:1 b:2). Press Enter to use default: ",
        'input_period_question': "Do you want to configure periods (moving averages and MACD)? (y/n): ",
        'input_mm_short': "Short moving average period (default 2): ",
        'input_mm_long': "Long moving average period (default 10): ",
        'input_macd_fast': "MACD fast period (default 12): ",
        'input_macd_slow': "MACD slow period (default 26): ",
        'input_macd_signal': "MACD signal period (default 9): ",
        'input_save_dir': "Enter directory to save files (or leave empty for default): ",
        'input_filename': "Enter base file name (or leave empty for random name): ",
        'input_save_hist': "Do you want to save user history? (y/n): ",
        'saving': "Saving results...",
        'success': "Analysis completed successfully!",
        'output_files': "Generated files:",
        'error': "Error: ",
        'goodbye': "Exiting. Goodbye!"
    },
    'frances': {
        'welcome': "Bienvenue à l'analyseur de lettres!",
        'lang_question': "Choisissez la langue : 1-Portugais, 2-Anglais, 3-Français, 4-Espagnol, 5-Arabe, 6-Italien",
        'lang_invalid': "Langue invalide. Utilisation du portugais.",
        'input_letters': "Entrez les lettres possibles séparées par des espaces (ex: a b c) : ",
        'input_responses': "Entrez la séquence de réponses (lettres séparées par des espaces) : ",
        'input_order_question': "Voulez-vous définir l'ordre (numéro 1-7) pour chaque lettre ? (o/n) : ",
        'input_order_manual': "Entrez au format 'lettre:numéro' (ex: a:1 b:2). Appuyez sur Entrée pour utiliser la valeur par défaut : ",
        'input_period_question': "Voulez-vous configurer les périodes (moyennes mobiles et MACD) ? (o/n) : ",
        'input_mm_short': "Période de la moyenne mobile courte (défaut 2) : ",
        'input_mm_long': "Période de la moyenne mobile longue (défaut 10) : ",
        'input_macd_fast': "Période rapide MACD (défaut 12) : ",
        'input_macd_slow': "Période lente MACD (défaut 26) : ",
        'input_macd_signal': "Période signal MACD (défaut 9) : ",
        'input_save_dir': "Entrez le répertoire pour sauvegarder les fichiers (ou laissez vide pour le défaut) : ",
        'input_filename': "Entrez le nom de base du fichier (ou laissez vide pour un nom aléatoire) : ",
        'input_save_hist': "Voulez-vous sauvegarder l'historique utilisateur ? (o/n) : ",
        'saving': "Sauvegarde des résultats...",
        'success': "Analyse terminée avec succès !",
        'output_files': "Fichiers générés :",
        'error': "Erreur : ",
        'goodbye': "Quitter. Au revoir !"
    },
    'espanhol': {
        'welcome': "¡Bienvenido al analizador de letras!",
        'lang_question': "Elige el idioma: 1-Portugués, 2-Inglés, 3-Francés, 4-Español, 5-Árabe, 6-Italiano",
        'lang_invalid': "Idioma no válido. Usando portugués.",
        'input_letters': "Ingrese las letras posibles separadas por espacios (ej: a b c): ",
        'input_responses': "Ingrese la secuencia de respuestas (letras separadas por espacios): ",
        'input_order_question': "¿Desea definir el orden (número 1-7) para cada letra? (s/n): ",
        'input_order_manual': "Ingrese en formato 'letra:número' (ej: a:1 b:2). Pulse Enter para usar el valor por defecto: ",
        'input_period_question': "¿Desea configurar los períodos (medias móviles y MACD)? (s/n): ",
        'input_mm_short': "Período de la media móvil corta (por defecto 2): ",
        'input_mm_long': "Período de la media móvil larga (por defecto 10): ",
        'input_macd_fast': "Período rápido MACD (por defecto 12): ",
        'input_macd_slow': "Período lento MACD (por defecto 26): ",
        'input_macd_signal': "Período señal MACD (por defecto 9): ",
        'input_save_dir': "Ingrese el directorio para guardar los archivos (o deje vacío para el predeterminado): ",
        'input_filename': "Ingrese el nombre base del archivo (o deje vacío para nombre aleatorio): ",
        'input_save_hist': "¿Desea guardar el historial del usuario? (s/n): ",
        'saving': "Guardando resultados...",
        'success': "¡Análisis completado con éxito!",
        'output_files': "Archivos generados:",
        'error': "Error: ",
        'goodbye': "Saliendo. ¡Hasta luego!"
    },
    'arabe': {
        'welcome': "مرحباً بكم في محلل الحروف!",
        'lang_question': "اختر اللغة: 1-البرتغالية، 2-الإنجليزية، 3-الفرنسية، 4-الإسبانية، 5-العربية، 6-الإيطالية",
        'lang_invalid': "لغة غير صالحة. سيتم استخدام البرتغالية.",
        'input_letters': "أدخل الحروف الممكنة مفصولة بمسافات (مثال: a b c): ",
        'input_responses': "أدخل تسلسل الإجابات (حروف مفصولة بمسافات): ",
        'input_order_question': "هل تريد تحديد الترتيب (رقم 1-7) لكل حرف؟ (نعم/لا): ",
        'input_order_manual': "أدخل بصيغة 'حرف:رقم' (مثال: a:1 b:2). اضغط Enter لاستخدام الافتراضي: ",
        'input_period_question': "هل تريد تكوين الفترات (المتوسطات المتحركة وMACD)؟ (نعم/لا): ",
        'input_mm_short': "فترة المتوسط المتحرك القصير (الافتراضي 2): ",
        'input_mm_long': "فترة المتوسط المتحرك الطويل (الافتراضي 10): ",
        'input_macd_fast': "فترة MACD السريعة (الافتراضي 12): ",
        'input_macd_slow': "فترة MACD البطيئة (الافتراضي 26): ",
        'input_macd_signal': "فترة إشارة MACD (الافتراضي 9): ",
        'input_save_dir': "أدخل المجلد لحفظ الملفات (أو اتركه فارغاً للافتراضي): ",
        'input_filename': "أدخل اسم الملف الأساسي (أو اتركه فارغاً لاسم عشوائي): ",
        'input_save_hist': "هل تريد حفظ سجل المستخدم؟ (نعم/لا): ",
        'saving': "جارٍ حفظ النتائج...",
        'success': "تم التحليل بنجاح!",
        'output_files': "الملفات المولدة:",
        'error': "خطأ: ",
        'goodbye': "الخروج. إلى اللقاء!"
    },
    'italiano': {
        'welcome': "Benvenuto all'analizzatore di lettere!",
        'lang_question': "Scegli la lingua: 1-Portoghese, 2-Inglese, 3-Francese, 4-Spagnolo, 5-Arabo, 6-Italiano",
        'lang_invalid': "Lingua non valida. Utilizzo del portoghese.",
        'input_letters': "Inserisci le lettere possibili separate da spazi (es: a b c): ",
        'input_responses': "Inserisci la sequenza di risposte (lettere separate da spazi): ",
        'input_order_question': "Vuoi definire l'ordine (numero 1-7) per ogni lettera? (s/n): ",
        'input_order_manual': "Inserisci nel formato 'lettera:numero' (es: a:1 b:2). Premi Invio per usare il default: ",
        'input_period_question': "Vuoi configurare i periodi (medie mobili e MACD)? (s/n): ",
        'input_mm_short': "Periodo della media mobile corta (default 2): ",
        'input_mm_long': "Periodo della media mobile lunga (default 10): ",
        'input_macd_fast': "Periodo rapido MACD (default 12): ",
        'input_macd_slow': "Periodo lento MACD (default 26): ",
        'input_macd_signal': "Periodo segnale MACD (default 9): ",
        'input_save_dir': "Inserisci la directory per salvare i file (o lascia vuoto per il default): ",
        'input_filename': "Inserisci il nome base del file (o lascia vuoto per nome casuale): ",
        'input_save_hist': "Vuoi salvare la cronologia utente? (s/n): ",
        'saving': "Salvataggio risultati...",
        'success': "Analisi completata con successo!",
        'output_files': "File generati:",
        'error': "Errore: ",
        'goodbye': "Uscita. Arrivederci!"
    }
}


# =======================================================
# FUNÇÕES AUXILIARES
# =======================================================
def traduzir(lang, chave):
    """Retorna a tradução da chave no idioma escolhido."""
    return TRADUCOES.get(lang, TRADUCOES['portugues']).get(chave, chave)


def get_lang():
    """Solicita e valida o idioma."""
    print("1. Português")
    print("2. Inglês")
    print("3. Francês")
    print("4. Espanhol")
    print("5. Árabe")
    print("6. Italiano")
    resp = input(traduzir('portugues', 'lang_question') + ": ")
    try:
        num = int(resp)
        mapping = {1: 'portugues', 2: 'ingles', 3: 'frances', 4: 'espanhol', 5: 'arabe', 6: 'italiano'}
        if num in mapping:
            return mapping[num]
        else:
            print(traduzir('portugues', 'lang_invalid'))
            return 'portugues'
    except:
        print(traduzir('portugues', 'lang_invalid'))
        return 'portugues'


def validar_entrada_sim_nao(prompt, lang):
    """Valida resposta sim/não."""
    resp = input(prompt).strip().lower()
    if resp in ['s', 'y', 'sim', 'yes', 'o', 'oui', 'نعم', 'sì']:
        return True
    elif resp in ['n', 'no', 'não', 'non', 'لا', 'no']:
        return False
    else:
        print(traduzir(lang, 'error') + " Resposta inválida. Tente novamente.")
        return validar_entrada_sim_nao(prompt, lang)


def input_int(prompt, default=None):
    """Lê um inteiro com validação e padrão opcional."""
    try:
        resp = input(prompt)
        if resp.strip() == "" and default is not None:
            return default
        return int(resp)
    except:
        if default is not None:
            print("Entrada inválida. Usando padrão:", default)
            return default
        else:
            print("Entrada inválida. Tente novamente.")
            return input_int(prompt, default)


def escolher_diretorio(prompt, lang, default_dir="."):
    """Escolhe diretório, com validação de existência."""
    dir_path = input(prompt).strip()
    if dir_path == "":
        return default_dir
    dir_path = os.path.expanduser(dir_path)
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
            print(traduzir(lang, 'saving') + f" Diretório criado: {dir_path}")
        except Exception as e:
            print(traduzir(lang, 'error') + f" {e}. Usando diretório padrão.")
            return default_dir
    return dir_path


# =======================================================
# FUNÇÕES DE CÁLCULO (mantidas da versão anterior)
# =======================================================
def calcular_ema(dados, periodo):
    ema = [dados[0]]
    multiplicador = 2 / (periodo + 1)
    for i in range(1, len(dados)):
        ema.append((dados[i] - ema[i - 1]) * multiplicador + ema[i - 1])
    return ema


def calcular_macd(dados, periodo_rapido=12, periodo_lento=26, periodo_sinal=9):
    ema_rapida = calcular_ema(dados, periodo_rapido)
    ema_lenta = calcular_ema(dados, periodo_lento)
    macd_line = [r - l for r, l in zip(ema_rapida, ema_lenta)]
    signal_line = calcular_ema(macd_line, periodo_sinal)
    hist_macd = [m - s for m, s in zip(macd_line, signal_line)]
    return macd_line, signal_line, hist_macd


def fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal):
    fvalor_x_tempo = []
    fvalor_y_repeticao = []
    fvalor_y_intensidadeOuLetra = []
    fOrdemRepeticao = []
    contador_repeticao = {letra: 0 for letra in vLetraRepeticao}

    for xResposta in vRespostas:
        if xResposta in vLetraRepeticao:
            fvalor_x_tempo.append(len(fvalor_x_tempo) + 1)
            contador_repeticao[xResposta] += 1
            fvalor_y_repeticao.append(contador_repeticao[xResposta])
            fvalor_y_intensidadeOuLetra.append(xResposta)
            if xResposta in vOrdemTotal:
                fOrdemRepeticao.append(vOrdemTotal[xResposta])
            else:
                fOrdemRepeticao.append(0)

    return [{
        'vXTempo': fvalor_x_tempo,
        'vYRepeticao': fvalor_y_repeticao,
        'vYLetra': fvalor_y_intensidadeOuLetra,
        'vRepeticao': fOrdemRepeticao
    }]


# =======================================================
# FUNÇÃO PRINCIPAL DE ANÁLISE E GERAÇÃO DE GRÁFICOS
# =======================================================
def executar_analise(config, lang):
    """Executa a análise com base na configuração fornecida."""
    vLetraRepeticao = config['letras']
    vTempoLetra = config['tempos'] if 'tempos' in config else []
    vRespostas = config['respostas']
    vOrdemTotal = config['ordem']

    vResux = fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal)
    dados = vResux[0]
    vRepeticao = dados['vRepeticao']  # valores numéricos (1-7)
    vX = dados['vXTempo']
    vLetras = dados['vYLetra']

    if len(vRepeticao) == 0:
        print(traduzir(lang, 'error') + " Sem dados para processar!")
        return None

    # Períodos
    mm_curto = config.get('mm_curto', 2)
    mm_longo = config.get('mm_longo', 10)
    macd_fast = config.get('macd_fast', 12)
    macd_slow = config.get('macd_slow', 26)
    macd_signal = config.get('macd_signal', 9)

    # Médias móveis
    fmedia_movel_curta = []
    fmedia_movel_longa = []
    for i in range(len(vRepeticao)):
        if i >= mm_curto - 1:
            janela_curta = vRepeticao[i - mm_curto + 1: i + 1]
            fmedia_movel_curta.append(sum(janela_curta) / len(janela_curta))
        else:
            fmedia_movel_curta.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

        if i >= mm_longo - 1:
            janela_longa = vRepeticao[i - mm_longo + 1: i + 1]
            fmedia_movel_longa.append(sum(janela_longa) / len(janela_longa))
        else:
            fmedia_movel_longa.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

    # Probabilidades normalizadas
    max_valor = max(vRepeticao) if vRepeticao else 1
    fprobabilidade_deox_curta = [m / max_valor for m in fmedia_movel_curta]
    fprobabilidade_deox_longa = [m / max_valor for m in fmedia_movel_longa]

    # Volume (variação absoluta)
    volume = [0]
    for i in range(1, len(vRepeticao)):
        volume.append(abs(vRepeticao[i] - vRepeticao[i - 1]))

    # MACD
    macd_line, signal_line, hist_macd = calcular_macd(vRepeticao, macd_fast, macd_slow, macd_signal)

    # =================== CRIAR GRÁFICOS ===================
    fig = plt.figure(figsize=(14, 14))

    # Subplot 1: Repetições e Médias Móveis
    ax1 = fig.add_subplot(5, 1, 1)
    ax1.plot(vX, vRepeticao, 'b-', label='Valor da Letra (1-7)', linewidth=2)
    ax1.plot(vX, fmedia_movel_curta, 'r--', label=f"MM Curta ({mm_curto})", linewidth=2)
    ax1.plot(vX, fmedia_movel_longa, 'g--', label=f"MM Longa ({mm_longo})", linewidth=2)
    ax1.set_xlabel('Tempo/Índice')
    ax1.set_ylabel('Valor de Repetição')
    ax1.set_title('1. Repetições e Médias Móveis')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Probabilidades Normalizadas
    ax2 = fig.add_subplot(5, 1, 2)
    ax2.plot(vX, fprobabilidade_deox_curta, 'r-', label='Prob. MM Curta', linewidth=2)
    ax2.plot(vX, fprobabilidade_deox_longa, 'g-', label='Prob. MM Longa', linewidth=2)
    ax2.set_xlabel('Tempo/Índice')
    ax2.set_ylabel('Probabilidade Normalizada')
    ax2.set_title('2. Probabilidades Normalizadas')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Subplot 3: Letras representadas por números (1-7)
    ax3 = fig.add_subplot(5, 1, 3)
    cores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    labels_numeros = ['1', '2', '3', '4', '5', '6', '7']
    for i in range(len(vX)):
        numero = vRepeticao[i]
        letra = vLetras[i]
        cor_idx = min(numero - 1, len(cores) - 1) if numero > 0 else 0
        cor = cores[cor_idx]
        ax3.scatter(vX[i], numero, c=cor, s=50, alpha=0.7)
        ax3.annotate(letra, (vX[i], numero), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax3.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax3.set_yticklabels(labels_numeros)
    if len(vX) > 1:
        z = np.polyfit(vX, vRepeticao, 1)
        p = np.poly1d(z)
        ax3.plot(vX, p(vX), "k--", alpha=0.5, label='Tendência Linear')
    ax3.set_xlabel('Tempo/Índice')
    ax3.set_ylabel('Número da Letra (1-7)')
    ax3.set_title('3. Letras Representadas por Números (1-7)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Legenda da letra→número
    legenda_texto = "Legenda:\n"
    for num in range(1, 8):
        letras_com_numero = [letra for letra, valor in vOrdemTotal.items() if valor == num]
        if letras_com_numero:
            legenda_texto += f"{num}: {', '.join(letras_com_numero)}\n"
    ax3.text(0.02, 0.98, legenda_texto, transform=ax3.transAxes,
             fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Subplot 4: Volume
    ax4 = fig.add_subplot(5, 1, 4)
    ax4.bar(vX, volume, color='steelblue', alpha=0.7, label='Volume (variação absoluta)')
    ax4.set_xlabel('Tempo/Índice')
    ax4.set_ylabel('Volume')
    ax4.set_title('4. Volume')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Subplot 5: MACD com Histograma
    ax5 = fig.add_subplot(5, 1, 5)
    ax5.plot(vX, macd_line, 'b-', label=f'MACD ({macd_fast},{macd_slow})', linewidth=2)
    ax5.plot(vX, signal_line, 'r-', label=f'Sinal ({macd_signal})', linewidth=2)
    cores_hist = ['green' if h >= 0 else 'red' for h in hist_macd]
    ax5.bar(vX, hist_macd, color=cores_hist, alpha=0.5, label='Histograma')
    ax5.axhline(0, color='black', linewidth=0.8)
    ax5.set_xlabel('Tempo/Índice')
    ax5.set_ylabel('MACD')
    ax5.set_title('5. MACD com Histograma')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    plt.tight_layout()

    # =================== SALVAR RESULTADOS ===================
    # Gerar nome base
    base_name = config['filename']
    if base_name == "":
        base_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # Diretório
    save_dir = config['save_dir']
    os.makedirs(save_dir, exist_ok=True)

    # Salvar figura
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fig_path = os.path.join(save_dir, f"{base_name}_{timestamp}.png")
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Salvar dados numéricos em CSV
    df = pd.DataFrame({
        'tempo': vX,
        'valor_letra': vRepeticao,
        'letra': vLetras,
        'mm_curta': fmedia_movel_curta,
        'mm_longa': fmedia_movel_longa,
        'prob_curta': fprobabilidade_deox_curta,
        'prob_longa': fprobabilidade_deox_longa,
        'volume': volume,
        'macd': macd_line,
        'signal': signal_line,
        'hist_macd': hist_macd
    })
    csv_path = os.path.join(save_dir, f"{base_name}_{timestamp}.csv")
    df.to_csv(csv_path, index=False)

    # Salvar configuração em JSON (para histórico)
    config_path = os.path.join(save_dir, f"{base_name}_{timestamp}_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # Salvar histórico do usuário
    if config['save_hist']:
        hist_dir = os.path.join(save_dir, "historico")
        os.makedirs(hist_dir, exist_ok=True)
        hist_path = os.path.join(hist_dir, f"historico_{timestamp}.json")
        user_data = {
            'timestamp': timestamp,
            'config': config,
            'resumo': {
                'num_pontos': len(vX),
                'ultimo_valor': vRepeticao[-1] if vRepeticao else None,
                'ultimo_macd': macd_line[-1] if macd_line else None
            }
        }
        with open(hist_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)

    return {
        'fig_path': fig_path,
        'csv_path': csv_path,
        'config_path': config_path,
        'dados': dados,
        'media_movel_curta': fmedia_movel_curta,
        'media_movel_longa': fmedia_movel_longa,
        'probabilidade_curta': fprobabilidade_deox_curta,
        'probabilidade_longa': fprobabilidade_deox_longa,
        'volume': volume,
        'macd_line': macd_line,
        'signal_line': signal_line,
        'hist_macd': hist_macd
    }


# =======================================================
# FUNÇÃO DE INTERAÇÃO COM O USUÁRIO (CLI)
# =======================================================
def interagir_usuario(lang):
    """Coleta configurações do usuário via input."""
    print(traduzir(lang, 'welcome'))

    # Coletar letras possíveis
    letras_str = input(traduzir(lang, 'input_letters')).strip()
    if not letras_str:
        print(traduzir(lang, 'error') + " Nenhuma letra fornecida. Usando padrão a b c.")
        letras = ['a', 'b', 'c']
    else:
        letras = letras_str.split()

    # Coletar respostas
    respostas_str = input(traduzir(lang, 'input_responses')).strip()
    if not respostas_str:
        print(traduzir(lang, 'error') + " Nenhuma resposta fornecida. Usando padrão a b c.")
        respostas = ['a', 'b', 'c']
    else:
        respostas = respostas_str.split()

    # Ordem das letras
    ordem = {}
    if validar_entrada_sim_nao(traduzir(lang, 'input_order_question'), lang):
        # Permitir definição manual
        ordem_str = input(traduzir(lang, 'input_order_manual')).strip()
        if ordem_str:
            for item in ordem_str.split():
                if ':' in item:
                    letra, num = item.split(':')
                    try:
                        ordem[letra.strip()] = int(num.strip())
                    except:
                        pass
        # Se não definiu todas, preencher padrão
        for letra in letras:
            if letra not in ordem:
                ordem[letra] = min(7, max(1, letras.index(letra) % 7 + 1))
    else:
        # Padrão: atribuir números sequenciais (1-7)
        for i, letra in enumerate(letras):
            ordem[letra] = (i % 7) + 1

    # Períodos
    mm_curto, mm_longo, macd_fast, macd_slow, macd_signal = 2, 10, 12, 26, 9
    if validar_entrada_sim_nao(traduzir(lang, 'input_period_question'), lang):
        mm_curto = input_int(traduzir(lang, 'input_mm_short'), 2)
        mm_longo = input_int(traduzir(lang, 'input_mm_long'), 10)
        macd_fast = input_int(traduzir(lang, 'input_macd_fast'), 12)
        macd_slow = input_int(traduzir(lang, 'input_macd_slow'), 26)
        macd_signal = input_int(traduzir(lang, 'input_macd_signal'), 9)

    # Diretório de saída
    save_dir = input(traduzir(lang, 'input_save_dir')).strip()
    if save_dir == "":
        save_dir = os.path.join(os.getcwd(), "resultados")
    save_dir = os.path.expanduser(save_dir)
    try:
        os.makedirs(save_dir, exist_ok=True)
    except:
        save_dir = os.getcwd()

    # Nome do arquivo
    filename = input(traduzir(lang, 'input_filename')).strip()
    if filename == "":
        filename = ""

    # Salvar histórico?
    save_hist = validar_entrada_sim_nao(traduzir(lang, 'input_save_hist'), lang)

    config = {
        'letras': letras,
        'respostas': respostas,
        'ordem': ordem,
        'mm_curto': mm_curto,
        'mm_longo': mm_longo,
        'macd_fast': macd_fast,
        'macd_slow': macd_slow,
        'macd_signal': macd_signal,
        'save_dir': save_dir,
        'filename': filename,
        'save_hist': save_hist,
        'lang': lang
    }
    return config


# =======================================================
# SEGURANÇA PARA SAÍDA ABRUPTA
# =======================================================
estado_atual = {}


def salvar_estado_emergencia():
    """Salva estado atual em caso de saída abrupta."""
    if estado_atual:
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(estado_atual.get('save_dir', '.'), f"estado_emergencia_{timestamp}.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(estado_atual, f, ensure_ascii=False, indent=2)
        except:
            pass


def handler_signal(signum, frame):
    salvar_estado_emergencia()
    sys.exit(1)


# Registrar handlers
signal.signal(signal.SIGINT, handler_signal)
signal.signal(signal.SIGTERM, handler_signal)
atexit.register(salvar_estado_emergencia)


# =======================================================
# MAIN
# =======================================================
def main():
    try:
        lang = get_lang()
        config = interagir_usuario(lang)

        # Atualizar estado global para emergência
        estado_atual.update(config)
        estado_atual['inicio'] = datetime.datetime.now().isoformat()

        print(traduzir(lang, 'saving'))
        resultado = executar_analise(config, lang)

        if resultado:
            print(traduzir(lang, 'success'))
            print(traduzir(lang, 'output_files'))
            for key in ['fig_path', 'csv_path', 'config_path']:
                if key in resultado:
                    print(f"  {key}: {resultado[key]}")
        else:
            print(traduzir(lang, 'error') + " Falha na análise.")

        # Limpar estado (não precisa mais)
        estado_atual.clear()

    except KeyboardInterrupt:
        salvar_estado_emergencia()
        print(traduzir(lang, 'goodbye') if 'lang' in estado_atual else "Encerrando.")
    except Exception as e:
        salvar_estado_emergencia()
        print(traduzir('portugues', 'error') + f" {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()