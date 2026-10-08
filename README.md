# Prosa Tech

Portfólio em Flask com um formulário de contato enviado por e-mail via Resend.

## Executar localmente

```bash
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Abra `http://127.0.0.1:5000`.

## Estilos do portfólio

As classes utilitárias usadas pelo template estão compiladas em
`static/tailwind.css`. O site não carrega o JavaScript do Tailwind por CDN em
tempo de execução.

## Configurar o formulário de contato

O projeto carrega as configurações do arquivo `.env` local. Crie uma conta no
[Resend](https://resend.com/), gere uma API key e informe o valor de
`RESEND_API_KEY` no `.env`. O endereço `onboarding@resend.dev` pode ser usado
para testes e só permite enviar para o endereço da própria conta Resend.
Para enviar para outros destinatários, verifique um domínio no Resend e use
um endereço desse domínio em `RESEND_FROM_EMAIL`.

```env
RESEND_API_KEY=re_xxxxxxxxx
RESEND_FROM_EMAIL=Prosa Tech <onboarding@resend.dev>
CONTACT_RECIPIENT=prosa.tech.cybersec@gmail.com
```

O envio usa o SDK oficial `resend` para Python (`resend.Emails.send`). O e-mail
do cliente é usado como `reply_to`; o remetente permanece o endereço verificado
no Resend.

O `.env` é ignorado pelo Git para proteger a chave. Reinicie o Flask depois de
preenchê-la. Sem a chave ou um remetente autorizado, o site continua disponível,
mas o formulário informa que o envio não está configurado.

Substitua `re_xxxxxxxxx` pela sua chave real do Resend no `.env` local. Não
coloque a chave neste código de exemplo nem compartilhe-a no chat ou no Git.
