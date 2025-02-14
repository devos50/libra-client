from command import *


class TransferCommand(Command):
    def get_aliases(self):
        return ["transfer", "transferb", "t", "tb"]

    def get_params_help(self):
        return ("\n\t<sender_account_address>|<sender_account_ref_id>"
         " <receiver_account_address>|<receiver_account_ref_id> <number_of_coins>"
         " [gas_unit_price_in_micro_libras (default=0)] [max_gas_amount_in_micro_libras (default 140000)]"
         " Suffix 'b' is for blocking. ")

    def get_description(self):
        return "Transfer coins (in libra) from account to another."

    def execute(self, client, params):
        if len(params) < 4 or len(params) > 6:
            print("Invalid number of arguments for transfer")
            print(
                "{} {}".format(
                    " | ".join(self.get_aliases()),
                    self.get_params_help()
                )
            )
            return
        try:
            if len(params) == 5:
                gas_unit_price_in_micro_libras = int(params[4])
            else:
                gas_unit_price_in_micro_libras = 0
            if len(params) == 6:
                max_gas_amount_in_micro_libras = int(params[5])
            else:
                max_gas_amount_in_micro_libras = 140_000
            print(">> Transferring")
            is_blocking = blocking_cmd(params[0])
            index, sequence_number = client.transfer_coins(params[1], params[2], params[3],
                max_gas_amount_in_micro_libras, gas_unit_price_in_micro_libras, is_blocking)
            if is_blocking:
                print("Finished transaction!")
            else:
                print("Transaction submitted to validator")
            print(
                "To query for transaction status, run: query txn_acc_seq {} {} \
                <fetch_events=true|false>".format(
                index, sequence_number
                )
            )
        except Exception as err:
            report_error("Failed to perform transaction", err)

