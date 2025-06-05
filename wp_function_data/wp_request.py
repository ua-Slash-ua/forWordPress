body_request= '''<?php

add_action('rest_api_init', function () {
    register_rest_route('responses/v1', '/LWORD/', [
        'methods' => 'POST',
        'callback' => 'handle_LWORD_submission',
        'permission_callback' => '__return_true',
    ]);
});

function handle_LWORD_submission(WP_REST_Request $request) {

}'''

send_email_func ='''
// function send_email($from, $subject, $message, $name_admin, $name_client, $file_path = null, $file_name = null) {
function send_email($from, $subject, $message, $name_client) {
    $mail = new PHPMailer(true);
    $to = 'SMTP_EMAIL';
    $name_admin = 'Slash Entertainment';
    try {
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->SMTPAuth = true;
        $mail->Username = $to;
        $mail->Password = SMTP_PASSWORD; // Використовуйте змінну з конфігурації
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
        $mail->Port = 465;

        $mail->setFrom($to, $name_admin);
        $mail->addAddress($from, $name_client);

        $mail->isHTML(true);
        $mail->Subject = $subject;
        $mail->Body = $message;

        // Перевірка та додавання файлу
        // if ($file_path && file_exists($file_path)) {
        //     $mail->addAttachment($file_path, $file_name ? $file_name : basename($file_path));
        // }

        $mail->send();
        return true;
    } catch (Exception $e) {
        error_log('Mail error: ' . $e->getMessage());
        return false;
    }
}
'''
send_email_incl = r'''
require_once __DIR__ .  '/../PATH/src/Exception.php';
require_once __DIR__ .  '/../PATH/src/PHPMailer.php';
require_once __DIR__ .  '/../PATH/src/SMTP.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;'''

standart_func_mail = '''
    $email = $request->get_param('email');
    $name = $request->get_param('names');
//    $file = $request->get_param('file');


    // Перевірка на порожні поля
    if (empty($email) || empty($name)) {
        return new WP_REST_Response([
            "status" => "error",
            "message" => "Email or name cannot be empty"
        ], 400); // Відправка 400 помилки
    } else {
        // Перевірка на правильність формату email
        if (!is_email($email)) {
            return new WP_REST_Response([
                "status" => "error",
                "message" => "Invalid email format"
            ], 400); // Відправка 400 помилки
        }
        $subject = 'Thank you for your order!!!';
        $message = 'Message for your order';
        error_log("Sending email to: $email with subject: $subject");
        if (send_email($email, $subject,$message,$name)) {
            return new WP_REST_Response([
                "status" => "success",
                "message" => "Form submission successful!!!",
            ], 200); // Успішна відповідь
        }else{
            return new WP_REST_Response([
                "status" => "error",
                "message" => "Error sending mail"
            ], 400); // Відправка 400 помилки
        }

    }'''