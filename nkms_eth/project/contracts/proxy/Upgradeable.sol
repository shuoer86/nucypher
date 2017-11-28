pragma solidity ^0.4.18;


import "../zeppelin/ownership/Ownable.sol";


/**
* @notice Base contract for upgradeable contract
* @dev Implementation contract should realize verifyState(address testTarget) method
* by checking storage variables (see verifyState(address testTarget) in Dispatcher)
**/
contract Upgradeable is Ownable {

    /**
    * @dev Contracts at the target must reserve the first location in storage for this address as
    * they will be called through this contract.
    * Stored data actually lives in the Dispatcher.
    * However the storage layout is specified here in the implementing contracts.
    **/
    address public target;
    /**
    * @dev Previous contract address (if available). Used for rollback
    **/
    address public previousTarget;

    /**
    * @dev Method for verifying storage state.
    * Should check that new target contract returns right storage value
    **/
    function verifyState(address testTarget) public;

    /**
    * @dev Simple method for call function without parameters.
    * Result should not exceed 32 bytes
    **/
    //TODO fix return size
    function delegateGet(address testTarget, string signature)
        internal returns (bytes32 result)
    {
        bytes4 targetCall = bytes4(keccak256(signature));
        assembly {
            let free := mload(0x40)
            mstore(free, targetCall)
            let retVal := delegatecall(gas, testTarget, free, 4, free, 32)
            result := mload(free)
        }
    }
}
