from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path

class Bot_ODS():
     
    def baixa_arquivos(self, Name, nome_do_arquivo):
        # Inicia o navegador
        navegador = webdriver.Chrome()
        navegador.get('https://www.cidadessustentaveis.org.br/paginas/idsc-br')

       
        wait = WebDriverWait(navegador, 20)

        # Abre o formulário de download
        wait.until(EC.element_to_be_clickable((By.XPATH, Name))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "cidade")))

        # Seleciona a cidade
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//mat-option//span[contains(text(), 'Santa Cruz do Sul - Rio Grande do Sul - Brasil')]"
        )))
        option.click()

        # Preenche os campos do formulário
        actions = webdriver.ActionChains(navegador)
        actions.send_keys(Keys.TAB).send_keys("lucasemgarth@gmail.com").send_keys(Keys.TAB)
        time.sleep(0.5)
        actions.send_keys("Leonardo André Muller").send_keys(Keys.TAB)
        time.sleep(0.5)
        actions.send_keys("Unisc").perform()

        time.sleep(3)

        # Clica no botão Confirmar
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Confirmar']]"))).click()

        # Aguarda o download
        time.sleep(8)
        
        while(self.verifica_arquivos(nome_do_arquivo)==False):
            time.sleep(5)
        
        navegador.quit()
    
    
    def verifica_arquivos(self, nome_do_arquivo):
        pasta = Path.home() / "Downloads"
        arquivo = pasta / nome_do_arquivo

        if arquivo.exists():
            
            return True
        else:
            
            return False 
    
    
    