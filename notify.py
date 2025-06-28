#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CTF Watcher com Notificações via Pushover

Este script monitora uma plataforma CTF (baseada em CTFd) em busca de novos
desafios. Quando um novo desafio é detectado, ele dispara um alerta sonoro
local e envia uma notificação instantânea para seus dispositivos via Pushover.
"""

import os
import argparse
import subprocess
import time
import sys
import requests

# --- Constantes ---
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

def get_all_paths(directory: str) -> set:
    """
    Mapeia recursivamente um diretório e retorna um conjunto com os caminhos
    relativos de todos os arquivos e subdiretórios.
    """
    all_paths = set()
    for root, dirs, files in os.walk(directory):
        for name in files:
            full_path = os.path.join(root, name)
            relative_path = os.path.relpath(full_path, directory)
            all_paths.add(relative_path)
        for name in dirs:
            full_path = os.path.join(root, name)
            relative_path = os.path.relpath(full_path, directory)
            all_paths.add(relative_path)
    return all_paths

def send_pushover_notification(new_item_paths: list, config: dict):
    """Envia uma notificação listando os novos itens via Pushover."""
    print("[*] Preparando para enviar notificação via Pushover...")
    try:
        items_list_str = "\n- ".join(new_item_paths)
        message_body = f"Novos conteúdos para '{config['ctf_name']}':\n\n- {items_list_str}"

        payload = {
            "token": config['pushover_api_token'],
            "user": config['pushover_user_key'],
            "title": "Novo Desafio de CTF Detectado!",
            "message": message_body,
            "sound": "persistent"
        }
        
        response = requests.post(PUSHOVER_API_URL, data=payload, timeout=10)

        if response.status_code == 200:
            print("[+] Notificação Pushover enviada com sucesso.")
        else:
            print(f"[ERRO] Falha ao enviar notificação. Status: {response.status_code}", file=sys.stderr)
            print(f"       Resposta: {response.text}", file=sys.stderr)
            
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Ocorreu um erro de conexão ao enviar a notificação: {e}", file=sys.stderr)
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro inesperado na função de notificação: {e}", file=sys.stderr)

def play_local_alert(sound_path: str):
    """Toca um arquivo de som usando comandos nativos do sistema operacional."""
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!   NOVO CONTEÚDO DETETADO!   !!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    
    if not os.path.exists(sound_path):
        print(f"[AVISO] Arquivo de som de alerta não encontrado em: {sound_path}", file=sys.stderr)
        return

    try:
        if sys.platform.startswith("linux"):
            subprocess.run(['aplay', '-q', sound_path], check=True)
        elif sys.platform == "darwin":
            subprocess.run(['afplay', sound_path], check=True)
        elif sys.platform == "win32":
            import winsound
            winsound.PlaySound(sound_path, winsound.SND_FILENAME)
        else:
            print("[INFO] Player de som padrão não configurado para este SO.", file=sys.stderr)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"[ERRO] Não foi possível tocar o som de alerta. Verifique se 'aplay' (Linux) ou 'afplay' (macOS) está instalado.", file=sys.stderr)
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro ao tentar tocar o som: {e}", file=sys.stderr)

def check_for_new_content(config: dict):
    """Verifica se há novo conteúdo no diretório do CTF após a sincronização."""
    challenges_path = os.path.join(config['output_dir'], config['ctf_name'])
    os.makedirs(challenges_path, exist_ok=True)
    
    before_paths = get_all_paths(challenges_path)

    command = [
        "ctfd-downloader",
        "-u", config['ctf_url'],
        "-n", config['ctf_name'],
        "-o", config['output_dir'],
        "-t", config['ctf_token'],
        "--update"
    ]

    print(f"[*] Verificando {config['ctf_url']} às {time.strftime('%H:%M:%S')}...")
    try:
        subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        after_paths = get_all_paths(challenges_path)
        new_items = sorted(list(after_paths - before_paths))

        if new_items:
            play_local_alert(config['alert_sound'])
            print("[+] Novo conteúdo encontrado:")
            for item in new_items:
                print(f"  - {item}")
            send_pushover_notification(new_items, config)
        else:
            print("[*] Nenhum conteúdo novo encontrado.")

    except FileNotFoundError:
        print("[FATAL] Comando 'ctfd-downloader' não encontrado.", file=sys.stderr)
        print("         Por favor, instale com: pip install ctfd-downloader", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] O ctfd-downloader falhou (código: {e.returncode}):", file=sys.stderr)
        print(f"       Stderr: {e.stderr}", file=sys.stderr)
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro inesperado: {e}", file=sys.stderr)

def main():
    """Função principal para configurar e iniciar o loop de monitoramento."""
    parser = argparse.ArgumentParser(
        description="Monitora uma plataforma CTF e envia notificações via Pushover.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--url', type=str, default="https://ctf.donotecho.dev", help="URL da plataforma CTF.")
    parser.add_argument('--ctf-name', type=str, default="ctf_name", help="Nome do CTF (usado para criar o diretório).")
    parser.add_argument('--dir', type=str, default=".", help="Diretório base para salvar os desafios.")
    parser.add_argument('--interval', type=int, default=15, help="Intervalo em segundos entre as verificações.")
    parser.add_argument('--sound', type=str, default="alert.wav", help="Caminho para o arquivo de som do alerta.")
    
    args = parser.parse_args()

    # Carrega as chaves a partir de variáveis de ambiente
    config = {
        'ctf_token': os.environ.get("CTF_TOKEN"),
        'pushover_api_token': os.environ.get("PUSHOVER_API_TOKEN"),
        'pushover_user_key': os.environ.get("PUSHOVER_USER_KEY"),
        'ctf_url': args.url,
        'ctf_name': args.ctf_name,
        'output_dir': args.dir,
        'check_interval': args.interval,
        'alert_sound': args.sound
    }

    if not all([config['ctf_token'], config['pushover_api_token'], config['pushover_user_key']]):
        print("[FATAL] Variáveis de ambiente não configuradas!", file=sys.stderr)
        print("         Certifique-se de definir CTF_TOKEN, PUSHOVER_API_TOKEN e PUSHOVER_USER_KEY.", file=sys.stderr)
        sys.exit(1)

    print("--- CTF Watcher com Notificações Pushover ---")
    print(f"[*] Monitorando: {config['ctf_url']}")
    print(f"[*] Salvando em: {os.path.join(config['output_dir'], config['ctf_name'])}")
    print(f"[*] Intervalo de verificação: {config['check_interval']} segundos")
    print("[*] Watcher iniciado. Pressione Ctrl+C para parar.")

    try:
        while True:
            check_for_new_content(config)
            time.sleep(config['check_interval'])
    except KeyboardInterrupt:
        print("\n[*] Watcher parado pelo usuário. Saindo.")
    except Exception as e:
        print(f"\n[FATAL] Um erro crítico ocorreu no loop principal: {e}", file=sys.stderr)
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
