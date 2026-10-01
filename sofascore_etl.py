from curl_cffi import requests
import pandas as pd
import time
from datetime import datetime

def extrair_dados_sofascore():
    # ==========================================================
    # CONFIGURAÇÃO: MUDE APENAS ESTES 5 CAMPOS PARA NOVA BUSCA
    # ==========================================================
    SEASON_ID = 0000 # ID da Temporada
    TEAM_ID = 0000 # ID do Time 
    PLAYER_ID = 0000 # ID do Jogador 
    
    NOME_JOGADOR = ""  # Nome que vai no arquivo final
    ANO = ""                # Ano que vai no arquivo final
    # ==========================================================

    NOME_ARQUIVO = f"desempenho_{NOME_JOGADOR}_{ANO}.xlsx"
    TOURNAMENT_ID = 325 # Brasileirão Série A (Fixo)

    dados_finais = []
    print(f"Iniciando extração universal para: {NOME_JOGADOR.upper()} ({ANO})...\n")

    session = requests.Session(impersonate="chrome110")

    for rodada in range(1, 39):
        print(f"Buscando Rodada {rodada}...")
        
        dados_rodada = {
            "Rodada": rodada, "Data Jogo": "-", "Nota SofaScore": "-", "Minutos Jogados": "-", 
            "Gols": "-", "Assistencia": "-", "Precisão nas finalizações": "-", "Passes certos": "-", 
            "Passes no campo adversário": "-", "Passes no próprio campo": "-", "Passes Decisivos": "-", 
            "Precisao nos cruzamentos": "-", "Precisao nos passes longos": "-", "Ações com a bola": "-", 
            "Domínios malsucedidos": "-", "Precisão nos dribles": "-", "Perda da posse de bola": "-", 
            "faltas sofridas": "-", "Contribuições def.": "-", "Precisão nos desarmes": "-", 
            "Interceptações": "-", "Cortes": "-", "Chutes defendidos": "-", "recuperação de bola": "-", 
            "Precisão nos duelos pelo chão": "-", "Precisão nos duelos pelo alto": "-",
            "Faltas Cometidas": "-", "Driblado": "-", "Cartão Amarelo": "-", "Cartão Vermelho": "-"
        }

        url_rodada = f"https://api.sofascore.com/api/v1/unique-tournament/{TOURNAMENT_ID}/season/{SEASON_ID}/events/round/{rodada}"
        
        for tentativa in range(1, 4):
            try:
                res_ev = session.get(url_rodada, timeout=25)
                if res_ev.status_code != 200: 
                    break
                    
                eventos = res_ev.json().get('events', [])
                jogo = next((e for e in eventos if e['homeTeam']['id'] == TEAM_ID or e['awayTeam']['id'] == TEAM_ID), None)
                
                if not jogo: 
                    break
                    
                event_id = jogo['id']
                dados_rodada["Data Jogo"] = datetime.fromtimestamp(jogo['startTimestamp']).strftime('%d/%m/%Y')
                
                res_lin = session.get(f"https://api.sofascore.com/api/v1/event/{event_id}/lineups", timeout=25)
                
                if res_lin.status_code == 200:
                    lineups = res_lin.json()
                    jogador_encontrado = False
                    
                    for lado in ['home', 'away']:
                        for j_data in lineups.get(lado, {}).get('players', []):
                            if j_data.get('player', {}).get('id') == PLAYER_ID:
                                jogador_encontrado = True
                                s = j_data.get('statistics', {})
                                
                                if not s: 
                                    break 
                                    
                                def fmt_p(certos, totais):
                                    if totais > 0:
                                        return f"{certos}/{totais} ({round((certos/totais)*100)}%)"
                                    return "0/0 (50%)"

                                # Processamento Ofensivo e Passes
                                f_tot = s.get("onTargetScoringAttempt", 0) + s.get("shotOffTarget", 0) + s.get("blockedScoringAttempt", 0)
                                p_finalizacoes = fmt_p(s.get("onTargetScoringAttempt", 0), f_tot)
                                p_certos = fmt_p(s.get("accuratePass", 0), s.get("totalPass", 0))
                                
                                p_adv = fmt_p(s.get("accurateOppositionHalfPasses", 0), s.get("totalOppositionHalfPasses", 0))
                                p_prop = fmt_p(s.get("accurateOwnHalfPasses", 0), s.get("totalOwnHalfPasses", 0))
                                
                                p_cruz = fmt_p(s.get("accurateCross", 0), s.get("totalCross", 0))
                                p_long = fmt_p(s.get("accurateLongBalls", 0), s.get("totalLongBalls", 0))
                                p_drib = fmt_p(s.get("wonContest", 0), s.get("totalContest", 0))
                                
                                # Processamento Defensivo
                                interceptacoes = s.get("interceptionWon", s.get("interceptions", 0))
                                cortes = s.get("totalClearance", 0)
                                chutes_defendidos = s.get("outfielderBlock", 0)
                                
                                des_tentados = s.get("totalTackle", 0)
                                des_ganhos = s.get("wonTackle", s.get("tackleWon", 0))
                                p_desarmes = fmt_p(des_ganhos, des_tentados)
                                
                                contrib_defensivas = s.get("defensiveActions", (des_tentados + interceptacoes + cortes + chutes_defendidos))
                                
                                # Duelos
                                a_won = s.get("aerialWon", 0)
                                a_tot = a_won + s.get("aerialLost", 0)
                                d_won = s.get("duelWon", 0)
                                d_tot = d_won + s.get("duelLost", 0)
                                p_alto = fmt_p(a_won, a_tot)
                                p_chao = fmt_p(max(0, d_won - a_won), max(0, d_tot - a_tot))

                                # Cartões (Busca no endpoint de incidentes)
                                am, ver = 0, 0
                                res_inc = session.get(f"https://api.sofascore.com/api/v1/event/{event_id}/incidents", timeout=25)
                                if res_inc.status_code == 200:
                                    for inc in res_inc.json().get('incidents', []):
                                        if inc.get('player', {}).get('id') == PLAYER_ID and inc.get('incidentType') == 'card':
                                            if inc.get('incidentClass') == 'yellow': am = 1
                                            elif inc.get('incidentClass') in ['red', 'yellowRed']: ver = 1

                                # Consolidação dos dados
                                dados_rodada.update({
                                    "Nota SofaScore": s.get("rating", "-"),
                                    "Minutos Jogados": s.get("minutesPlayed", "-"),
                                    "Gols": s.get("goals", 0),
                                    "Assistencia": s.get("goalAssist", 0),
                                    "Precisão nas finalizações": p_finalizacoes,
                                    "Passes certos": p_certos,
                                    "Passes no campo adversário": p_adv,
                                    "Passes no próprio campo": p_prop,
                                    "Passes Decisivos": s.get("keyPass", 0),
                                    "Precisao nos cruzamentos": p_cruz,
                                    "Precisao nos passes longos": p_long,
                                    "Ações com a bola": s.get("touches", 0),
                                    "Domínios malsucedidos": s.get("unsuccessfulTouch", 0), 
                                    "Precisão nos dribles": p_drib,
                                    "Perda da posse de bola": s.get("possessionLostCtrl", 0),
                                    "faltas sofridas": s.get("wasFouled", 0),
                                    "Contribuições def.": contrib_defensivas,
                                    "Precisão nos desarmes": p_desarmes,
                                    "Interceptações": interceptacoes,
                                    "Cortes": cortes,
                                    "Chutes defendidos": chutes_defendidos,
                                    "recuperação de bola": s.get("ballRecovery", 0),
                                    "Precisão nos duelos pelo chão": p_chao,
                                    "Precisão nos duelos pelo alto": p_alto,
                                    "Faltas Cometidas": s.get("fouls", 0),
                                    "Driblado": s.get("challengeLost", 0),
                                    "Cartão Amarelo": am, "Cartão Vermelho": ver
                                })
                                print(f"  -> Estatísticas extraídas com sucesso! Nota: {s.get('rating')}")
                                break
                        if jogador_encontrado: 
                            break
                            
                    if not jogador_encontrado: 
                        print("  -> Atleta não relacionado ou no banco.")
                break 
                
            except Exception as e:
                if tentativa == 3: 
                    print(f"  -> Erro fatal após 3 tentativas: {e}")
                time.sleep(2)

        dados_finais.append(dados_rodada)
        time.sleep(1.2)

    df = pd.DataFrame(dados_finais)
    df.to_excel(NOME_ARQUIVO, index=False)
    print(f"\n✅ Extração concluída! Planilha '{NOME_ARQUIVO}' gerada com sucesso.")

if __name__ == "__main__":
    extrair_dados_sofascore()