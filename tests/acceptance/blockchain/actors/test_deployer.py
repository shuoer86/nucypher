


import json

import pytest
import random

from nucypher.config.constants import TEMPORARY_DOMAIN
from nucypher.crypto.powers import TransactingPower
from nucypher.blockchain.eth.actors import ContractAdministrator
from nucypher.blockchain.eth.signers.software import Web3Signer
from tests.constants import NUMBER_OF_ALLOCATIONS_IN_TESTS

# Prevents TesterBlockchain to be picked up by py.test as a test class
from tests.utils.blockchain import TesterBlockchain as _TesterBlockchain


@pytest.mark.skip()
@pytest.mark.usefixtures('testerchain')
def test_rapid_deployment(application_economics, test_registry, temp_dir_path, get_random_checksum_address):

    blockchain = _TesterBlockchain(eth_airdrop=False, test_accounts=4)

    deployer_address = blockchain.etherbase_account
    deployer_power = TransactingPower(signer=Web3Signer(blockchain.client), account=deployer_address)

    administrator = ContractAdministrator(transacting_power=deployer_power,
                                          domain=TEMPORARY_DOMAIN,
                                          registry=test_registry)
    blockchain.bootstrap_network(registry=test_registry)

    all_yall = blockchain.unassigned_accounts

    # Start with some hard-coded cases...
    allocation_data = [{'checksum_address': all_yall[1],
                        'amount': application_economics.maximum_allowed_locked,
                        'lock_periods': application_economics.min_operator_seconds},

                       {'checksum_address': all_yall[2],
                        'amount': application_economics.min_authorization,
                        'lock_periods': application_economics.min_operator_seconds},

                       {'checksum_address': all_yall[3],
                        'amount': application_economics.min_authorization * 100,
                        'lock_periods': application_economics.min_operator_seconds},
                       ]

    # Pile on the rest
    for _ in range(NUMBER_OF_ALLOCATIONS_IN_TESTS - len(allocation_data)):
        checksum_address = get_random_checksum_address()
        amount = random.randint(application_economics.min_authorization, application_economics.maximum_allowed_locked)
        duration = random.randint(application_economics.min_operator_seconds, application_economics.maximum_rewarded_periods)
        random_allocation = {'checksum_address': checksum_address, 'amount': amount, 'lock_periods': duration}
        allocation_data.append(random_allocation)

    filepath = temp_dir_path / "allocations.json"
    with open(filepath, 'w') as f:
        json.dump(allocation_data, f)

    minimum, default, maximum = 10, 20, 30
    administrator.set_fee_rate_range(minimum, default, maximum)
