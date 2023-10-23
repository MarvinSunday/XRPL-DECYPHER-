from typing import Union
from xrpl.asyncio.clients import AsyncJsonRpcClient
import requests
from xrpl.asyncio.clients.client import Client
from xrpl.models import (AccountObjects, IssuedCurrencyAmount, NFTBuyOffers,
                         NFTokenAcceptOffer, NFTokenCancelOffer,
                         NFTokenCreateOffer, NFTokenCreateOfferFlag,
                         NFTSellOffers)
from xrpl.utils import drops_to_xrp, ripple_time_to_datetime, xrp_to_drops

from Misc import mm
from x_constants import M_SOURCE_TAG

"""nft handler"""



def create_sell_offer(sender_addr: str, nftoken_id: str, get: Union[float, IssuedCurrencyAmount], expiry_date: int = None, receiver: str = None, fee: str = None) -> dict:
    """create an nft sell offer, receiver is the account you want to match this offer"""
    amount = get
    if isinstance(get, float):
        amount = xrp_to_drops(get)
    txn = NFTokenCreateOffer(
        account=sender_addr,
        nftoken_id=nftoken_id,
        amount=amount,
        expiration=expiry_date,
        destination=receiver,
        flags=NFTokenCreateOfferFlag.TF_SELL_NFTOKEN, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()

def create_buy_offer(sender_addr: str, nftoken_id: str, give: Union[float, IssuedCurrencyAmount], expiry_date: int = None, receiver: str = None, fee: str = None) -> dict:
    """create an nft buy offer, receiver is the account you want to match this offer"""
    amount = give
    if isinstance(give, float):
        amount = xrp_to_drops(give)
    txn = NFTokenCreateOffer(
        account=sender_addr,
        nftoken_id=nftoken_id,
        amount=amount,
        expiration=expiry_date,
        destination=receiver, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl()          

def cancel_nft_offer(sender_addr: str, nftoken_offer_ids: list[str], fee: str = None) -> dict:
    """cancel offer, pass offer or offers id in a list"""
    txn = NFTokenCancelOffer(
        account=sender_addr,
        nftoken_offers=nftoken_offer_ids, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl() 

def accept_nft_offer(sender_addr: str, sell_offer_id: str = None, buy_offer_id: str = None, broker_fee: Union[IssuedCurrencyAmount, float] = None, fee: str = None) -> dict:
    """accept an nft sell or buy offer, or both simultaneously and charge a fee"""
    amount = broker_fee
    if isinstance(broker_fee, float):
        amount = xrp_to_drops(broker_fee)
    txn = NFTokenAcceptOffer(
        account=sender_addr,
        nftoken_buy_offer=buy_offer_id,
        nftoken_sell_offer=sell_offer_id,
        nftoken_broker_fee=amount, fee=fee, memos=mm(), source_tag=M_SOURCE_TAG)
    return txn.to_xrpl() 
