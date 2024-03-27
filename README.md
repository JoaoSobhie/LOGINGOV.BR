# LOGINGOV.BR
Esse repósitorio contem o código para realizar o login com certificado digital evitando o sistema anti-bot do gov.br.
Algumas configurações são necessárias para evitar hcaptcha e a identificação de execução via Script

# Sobre o GOV.BR
O gov.br utiliza o Canvas Fingerprint para identificar o comportamento do usuário em relação ao site, além de hcaptcha para realização do login.
A configuração do robô sera fundamental para a execução com sucesso.

## Configurando Robôs
Utilize o Brave Browser, ele evita fingerprints além de outros rastreadores que podem afetar no acesso robotizado sem hcaptcha.
## Executando dessa forma não está sendo solicitado hcaptcha, mas caso apareça, utilizo o death by captcha para solução
O Playwright apresentou o melhor resultado em benchmark, então é recomendado utiliza-lo
Use os seguintes argumentos na execução:
## "--no-sandbox"
## "--disable-setuid-sandbox"
## "--no-first-run"
## "--safebrowsing-disable-download-protection"
## "--disable-blink-features=AutomationControlled"
## "--start-normal"
## "--mute-audio"

# Certificado Digital
O Playwright não consegue selecionar o  certificado digital quando aparece o pop-up  da escolha do certificado. Para contornar a situação é necessário alterar o chrome policy "AutoSelectCertificateForUrls". No Linux ele fica localizado em "/etc/opt/chrome/policies/managed/managed_policy.json". No Windows, é necessario abrir o regedit e ir para Software\Policies\Google\Chrome\AutoSelectCertificateForUrls. Basta editar esse arquivo ou criar um novo com a seguinte configuração:
{
  "AutoSelectCertificateForUrls": ["{\"pattern\":\"*\",\"filter\":{}}"]
}

# Executando em Python 3.11