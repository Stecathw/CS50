///////////////////////////////////////////////////////////////////////
//--------------- MAIN NAVIGATION BUTTONS AND ACTIONS ---------------//
///////////////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Use submit button to send an email
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

///////////////////////////////////////////////////////////////////////
//---------------------- COMPOSE AN EMAIL VIEW ----------------------//
///////////////////////////////////////////////////////////////////////

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}


///////////////////////////////////////////////////////////////////////
//---- DISPLAYING ALL INBOX or SENT or ARCHIVED EMAILS AS A LIST ----//
///////////////////////////////////////////////////////////////////////

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // API request
  fetch(`/emails/${mailbox}`)
  .then((response) => response.json())
  .then((emails) => {
    console.log(emails);
    emails.forEach(email => {

      // Generate new divs with emails infos
      display_email(email, mailbox);

    });
  })
  .catch((error) => console.log(error));
}


///////////////////////////////////////////////////////////////////////
//------------------- CREATING EMAIL LIST ELEMENT -------------------//
///////////////////////////////////////////////////////////////////////

function display_email(email, mailbox) {

  // Each mail is rendered in its own box (as a <div> with a border).
  var mail = document.createElement('div');
  mail.className = "row row-cols-3";

  // Add mail to DOM
  document.querySelector('#emails-view').append(mail);

  // Populate the mail container div with the senders
  var mail_recip = document.createElement('div');
  mail_recip.className = "col text-left text-muted";
  if (mailbox === 'sent') {
    mail_recip.innerHTML = `To: ${email.recipients}`;
  } else {
    mail_recip.innerHTML = `From: ${email.sender}`;
  }
    
  // Populate the mail container div with the subject
  var mail_subj = document.createElement('div');
  mail_subj.className = "col text-left";
  mail_subj.innerHTML = `${email.subject}`;

  // Populate the mail container div with the timestamp
  var mail_ts = document.createElement('div');
  mail_ts.className = "col text-right text-muted";
  mail_ts.innerHTML = `${email.timestamp}`;
  
  // Appends all infos to mail container
  mail.append(mail_recip, mail_subj, mail_ts); 

  // Div styling background, by default background is white with bold police for all email
  mail.style.background = "white";
  mail_subj.style.fontWeight = "bold";
  mail_ts.style.fontStyle = "italic";

  // Once read it is grey with normal police
  if (email.read === true) {
    mail.style.background = "#e9ecef";
    mail_subj.style.fontWeight ="normal";
  } 

  // Allow user to open and read a mail
  mail.addEventListener('click', function() {
    view_email(email, mailbox);
    // if mail is read for the first time or a reply isnt read, updates mail status to "unread"
    if (!email.read) {
      mail_is_read(email);
    }
  });
}


///////////////////////////////////////////////////////////////////////
//------------------ SINGLE EMAIL VIEW AND READING ------------------//
///////////////////////////////////////////////////////////////////////

function view_email(email, mailbox) {

  // Reset mail-view
  document.querySelector('#mail-view').innerHTML = '';

  // Shows the mail view and hides the others
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'block';

  // Show the mailbox name
  document.querySelector('#mail-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Creates emails infos div and body (text) div
  const email_infos = document.createElement('div');
  email_infos.className = "email_infos";

  // Creates email text div
  const email_text = document.createElement('div');
  email_text.className ="email_text";

  // Email sender is always displayed
  const email_sender = document.createElement('div');
  email_sender.className = "sender";
  email_sender.innerHTML = "From: ";

  // Email recipients is always displayed
  const email_recip = document.createElement('div');
  email_recip.className = "to";
  email_recip.innerHTML = "To: ";

  // Subject is always displayed 
  const email_subj = document.createElement('div');
  email_subj.className = "subject";
  email_subj.innerHTML = "Subject: ";

  // Timestamp is always displayed
  const email_ts = document.createElement('div');
  email_ts.className ="ts";
  email_ts.innerHTML = "Date: ";

  // Div for archiving and replying buttons
  const buttons = document.createElement('div'); 
  buttons.className = "arch_and_reply"; 

  // Separation with email text
  const hr = document.createElement('hr');
  
  // Appends divs to email infos
  email_infos.append(email_sender, email_recip, email_subj, email_ts, buttons, hr);
  
  // Append email infos and email text to mail view
  document.querySelector("#mail-view").append(email_infos, email_text);   

  // API request
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {

    // Print email for debugging purpose
    console.log(email);

    // Email send by
    var sender = document.createElement('span');
    sender.innerHTML = `${email.sender}`;
    sender.style.fontWeight = "normal";
    email_sender.appendChild(sender);

    // Email to
    var recipients = document.createElement('span');
    recipients.innerHTML = `${email.recipients}`;
    recipients.style.fontWeight = "normal";
    email_recip.appendChild(recipients);

    // Email subject
    var subject = document.createElement('span');
    subject.innerHTML = `${email.subject}`;
    subject.style.fontWeight = "normal";
    email_subj.appendChild(subject);

    // Email timestamp
    var timestamp = document.createElement('span');
    timestamp.innerHTML = `${email.timestamp}`;
    timestamp.style.fontWeight = "normal";
    email_ts.appendChild(timestamp);
    
    // Email text
    var text = document.createElement('p');
    text.innerHTML = `${email.body}`;
    email_text.append(text);    

    // Check email archive status and display button accordingly
    var archive = document.createElement('button');
    if (email.archived === false) {
      archive.innerHTML = "Archive";
    } else {
      archive.innerHTML = "Unarchive";      
    }
    archive.className = "btn btn-sm btn-outline-secondary";
    archive.style.marginRight = "0.2rem";

    // Add a reply button
    const reply = document.createElement('button');
    reply.innerHTML = "Reply";
    reply.className = "btn btn-sm btn-outline-secondary";    

    // Allow archiving mail and reply to
    document.querySelector('.arch_and_reply').append(archive, reply);
    archive.addEventListener('click', () => archive_email(email));
    reply.addEventListener('click', () => reply_to(email));
  })    
  .catch((error) => console.log(error));
}


///////////////////////////////////////////////////////////////////////
//-------------------- EMAIL READ STATUS CHANGE ---------------------//
///////////////////////////////////////////////////////////////////////

function mail_is_read(email) {

  // API request
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      // Status change
      read: !email.read
    })
  })
  .catch((error) => console.log(error));
}


///////////////////////////////////////////////////////////////////////
//---------------------- SEND AN EMAIL ACTION -----------------------//
///////////////////////////////////////////////////////////////////////

function send_email() {
  
  // Store email informations
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value

  // API request
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  })
  // Show the mailbox with sent mails
  .then(() => load_mailbox('sent'))
  .catch((error) => console.log(error));

  // Stop submitting
  return false;
}

///////////////////////////////////////////////////////////////////////
//------------------- ARCHIVE EMAIL STATUS CHANGE -------------------//
///////////////////////////////////////////////////////////////////////

function archive_email(email) {
  
  // API request
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      // Status change
      archived: !email.archived
    })  
  }) 
  // Redirect to inbox page
  .then(() => load_mailbox('inbox'))  
}


///////////////////////////////////////////////////////////////////////
//------------------------ REPLY TO AN EMAIL ------------------------//
///////////////////////////////////////////////////////////////////////

function reply_to(email) {

  // Form to send an email
  compose_email();

  // Prefill form with recipients, subject timestamp and body
  document.querySelector('#compose-recipients').value = email.sender;
  if (email.subject.slice(0,3) === 'RE:') {
    document.querySelector('#compose-subject').value = email.subject;
  }
  else {
    document.querySelector('#compose-subject').value = `RE: ${email.subject}`;
  }
  document.querySelector('#compose-body').value = `\n\n------\nOn ${email.timestamp} ${email.sender} wrote:\n\n${email.body}`;


}
