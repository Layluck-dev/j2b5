
from pprint import pp
from typing import Any, Tuple
import uuid

from ..types import TransActionOutput, TransactionData

class TransActionInput:
    def validateBalance(self, balance: float, amount: float) -> float:
        return balance-amount
    
    def generateKey(self, balance: float, amount: float, isRemainder: bool) -> str:
        return f"{balance}{str(isRemainder)}{amount}"
    
    def generateOutputs(self, transaction: TransactionData) -> Tuple[TransActionOutput, TransActionOutput] | None:    
        remainder = self.validateBalance(transaction["balance"], transaction["amount"])
        
        if remainder < 0:
            return None
        
        commonId = str(uuid.uuid4())
        
        outputTransaction: TransActionOutput = {
            "id":           commonId,
            "hash":         self.generateKey(transaction["balance"], transaction["amount"], False),
            "amount":       transaction["amount"],
            "isRemainder":  False
        }
        
        outputRemainder: TransActionOutput = {
            "id":           commonId,
            "hash":         self.generateKey(transaction["balance"], transaction["amount"], True),
            "amount":       remainder,
            "isRemainder":  True
        }
        
        return (outputTransaction, outputRemainder)