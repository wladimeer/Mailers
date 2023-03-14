from flask import Blueprint, render_template, redirect, url_for, request, current_app
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from .schemas import email

blueprint_email = Blueprint('email', __name__, url_prefix='/')

@blueprint_email.route('/', methods=['GET'])
def index():
  search = request.args.get('search')

  if search is None:
    emails = email.read()
    
  else:
    emails = email.find_by_content(search)

    if len(emails) == 0: emails = email.read()

  return render_template('email/index.html', emails=emails)

@blueprint_email.route('/email/new_email', methods=['GET', 'POST'])
def new_email():
  if request.method == 'POST':
    address = request.form.get('address').strip()
    subject = request.form.get('subject').strip()
    content = request.form.get('content').strip()
    fields = {}
    error = []

    if len(address) == 0:
      error.append('Verifica la dirección de correo')
    else:
      fields['address'] = address

    if len(subject) == 0:
      error.append('Verifica el asunto del correo')
    else:
      fields['subject'] = subject

    if len(content) == 0:
      error.append('Verifica el contenido del correo')
    else:
      fields['content'] = content

    if len(error) > 0:
      message = {'error': error}

      return render_template('email/new_email.html', message=message, fields=fields)

    else:
      address = address.lower()
      subject = subject.title()
      content_text = ''
      # success = []
      error = []

      for value in content.split():
        content_text += value if value.startswith(',') or value.startswith('.')  else f' {value}'

      content = content_text.lstrip()

      response = send_email(to_emails=address, subject=subject, content=content)

      if response:
        response = email.create(address, subject, content)

        if response:
          # success.append('El correo fue enviado con éxito')
          # message = {'success': success}
          return redirect(url_for('email.index'))
        
        else:
          error.append('Ocurrio un error al guardar el correo')
          message = {'error': error}

          return render_template('email/new_email.html', message=message)
        
      else:
        error.append('Ocurrio un error al enviar el correo')
        message = {'error': error}

        return render_template('email/new_email.html', message=message)

  return render_template('email/new_email.html')

def send_email(to_emails, subject, content):
  api_key = current_app.config['SENDGRID_API_KEY']
  
  from_email = (current_app.config['FROM_EMAIL'], 'Sebastián')
  html_content = f'<div>{content}</div>'
  
  message = Mail(
    from_email=from_email,
    to_emails=to_emails,
    subject=subject,
    html_content=html_content
  )
  
  send_grid = SendGridAPIClient(api_key)
  response = send_grid.send(message)

  if response.status_code == 202:
    return True
  else:
    return False
