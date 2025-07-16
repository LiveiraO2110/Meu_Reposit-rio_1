from aplicacao import Aplicacao

if __name__ == "__main__":
    try:
        import selenium
        import pandas
    except ImportError:
        print("A biblioteca 'selenium' não está instalada. Rode: pip install -r requirements.txt")
        exit()
    
    app = Aplicacao()
    app.mainloop()