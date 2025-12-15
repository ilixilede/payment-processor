import logging
import os

from payment_processor.config import Config
from payment_processor.models import Payment
from payment_processor.payment_gateway import PaymentGateway
from payment_processor.repository import PaymentRepository
from payment_processor.services import PaymentService

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting payment processor')

    config = Config(os.environ.get('PAYMENT_PROCESSOR_CONFIG'))
    payment_gateway = PaymentGateway(config.payment_gateway)
    payment_repository = PaymentRepository(config.database_url)
    payment_service = PaymentService(payment_gateway, payment_repository)

    while True:
        payment = payment_service.get_pending_payment()
        if payment:
            logging.info(f'Processing payment {payment.id}')
            payment_service.process_payment(payment)
            logging.info(f'Payment {payment.id} processed successfully')
        else:
            logging.info('No pending payments found')
        logging.info('Sleeping for 10 seconds')
        import time
        time.sleep(10)

if __name__ == '__main__':
    main()