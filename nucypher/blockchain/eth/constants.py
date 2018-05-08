NULL_ADDRESS = '0x' + '0' * 40


class NuCypherTokenConfig:

    class TokenConfigError(ValueError):
        pass

    __subdigits = 18
    _M = 10 ** __subdigits                                 # Unit designation
    __initial_supply = int(1e9) * _M                       # Initial token supply
    __saturation = int(3.89e9) * _M                        # Token supply cap
    _remaining_supply = __saturation - __initial_supply    # Remaining supply

    @property
    def saturation(self):
        return self.__saturation


class NuCypherMinerConfig:

    class MinerConfigError(ValueError):
        pass

    _hours_per_period = 24       # Hours in single period
    _min_locked_periods = 30     # 720 Hours minimum
    __max_minting_periods = 365  # Maximum number of periods

    _min_allowed_locked = 15000 * NuCypherTokenConfig._M
    _max_allowed_locked = int(4e6) * NuCypherTokenConfig._M

    __remaining_supply = NuCypherTokenConfig._remaining_supply

    __mining_coeff = [           # TODO
        _hours_per_period,
        2 * 10 ** 7,
        __max_minting_periods,
        __max_minting_periods,
        _min_locked_periods,
        _min_allowed_locked,
        _max_allowed_locked
    ]

    @property
    def mining_coefficient(self):
        return self.__mining_coeff

    @property
    def remaining_supply(self):
        return self.__remaining_supply

    def __validate(self, rulebook) -> bool:
        for rule, failure_message in rulebook:
            if not rule:
                raise self.MinerConfigError(failure_message)
        return True

    def validate_stake_amount(self, amount: int, raise_on_fail=True) -> bool:

        rulebook = (

            (amount >= self._min_allowed_locked,
             'Stake amount too low; ({amount}) must be at least {minimum}'
             .format(minimum=self._min_allowed_locked, amount=amount)),

            (amount <= self._max_allowed_locked,
             'Stake amount too high; ({amount}) must be no more than {maximum}.'
             .format(maximum=self._max_allowed_locked, amount=amount)),
        )

        if raise_on_fail is True:
            self.__validate(rulebook=rulebook)
        return all(rulebook)

    def validate_locktime(self, periods: int, raise_on_fail=True) -> bool:

        rulebook = (

            (periods >= self._min_locked_periods,
             'Locktime ({locktime}) too short; must be at least {minimum}'
             .format(minimum=self._min_locked_periods, locktime=periods)),


            (periods <= self.__max_minting_periods,
             'Locktime ({locktime}) too long; must be no more than {maximum}'
             .format(maximum=self._min_locked_periods, locktime=periods)),
        )

        if raise_on_fail is True:
            self.__validate(rulebook=rulebook)
        return all(rulebook)
