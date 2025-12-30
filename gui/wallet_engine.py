from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class WalletAccount:
    """Lightweight representation of a wallet account for a single coin."""

    coin: str
    address: str
    balance: float
    pending: List[str] = field(default_factory=list)


@dataclass
class NodeConfig:
    """Connection details for a bring-your-own full node."""

    symbol: str
    rpc_address: str
    tls: bool = True

    def display_label(self) -> str:
        scheme = "https" if self.tls else "http"
        return f"{scheme}://{self.rpc_address}"


@dataclass
class WalletProfile:
    """Represents the locally held seed material and display name."""

    name: str
    seed_phrase: str


class WalletEngine:
    """Offline-first wallet engine used by the GUI layer.

    The engine keeps state in memory and enforces simple validation rules so the
    UI never touches storage or network resources directly. This mirrors the
    trust boundaries defined in the Kernel Wallet documentation: UI delegates
    validations and transaction building to the engine, which can later be
    swapped for a fully featured implementation without changing the GUI.

    The APIs are structured for production readiness: profile and node
    configuration must be loaded explicitly, validations are deterministic, and
    no network I/O is performed in this module.
    """

    def __init__(self) -> None:
        self._profile: Optional[WalletProfile] = None
        self._accounts: Dict[str, WalletAccount] = {
            "LTC": WalletAccount(
                coin="Litecoin",
                address="ltc1qd0mainsignalsample000000000000",
                balance=12.5,
            ),
            "XMR": WalletAccount(
                coin="Monero",
                address="48ExampleMoneroAddressPlaceholderMain00000000",
                balance=8.0,
            ),
        }
        self._node_configs: Dict[str, NodeConfig] = {}
        self._fee_bounds: Dict[str, Tuple[float, float]] = {
            "LTC": (0.0001, 0.01),
            "XMR": (0.00005, 0.02),
        }

    # Wallet identity management
    def has_profile(self) -> bool:
        return self._profile is not None

    def set_profile(self, name: str, seed_phrase: str) -> WalletProfile:
        cleaned_name = name.strip()
        cleaned_seed = " ".join(seed_phrase.strip().split())

        if not cleaned_name:
            raise ValueError("Wallet name is required.")

        words = cleaned_seed.split()
        word_count = len(words)
        if word_count < 12 or word_count > 24:
            raise ValueError("Seed phrase must contain between 12 and 24 words.")
        if any(not word.isalpha() for word in words):
            raise ValueError("Seed phrase should contain only alphabetic words.")

        self._profile = WalletProfile(name=cleaned_name, seed_phrase=cleaned_seed)
        return self._profile

    def get_profile(self) -> WalletProfile:
        if not self._profile:
            raise ValueError("No wallet profile is loaded.")
        return self._profile

    def list_accounts(self) -> List[WalletAccount]:
        return list(self._accounts.values())

    def get_account(self, symbol: str) -> WalletAccount:
        if symbol not in self._accounts:
            raise KeyError(f"Unsupported asset: {symbol}")
        return self._accounts[symbol]

    def set_node(self, symbol: str, rpc_address: str, tls: bool = True) -> NodeConfig:
        if symbol not in self._accounts:
            raise KeyError(f"Unsupported asset: {symbol}")

        clean_address = rpc_address.strip()
        if not clean_address:
            raise ValueError("Node endpoint is required for production use.")
        if ":" in clean_address:
            host, _, port = clean_address.partition(":")
            if not host or not port.isdigit():
                raise ValueError("Node endpoint must use host:port form without a scheme.")

        node = NodeConfig(symbol=symbol, rpc_address=clean_address, tls=bool(tls))
        self._node_configs[symbol] = node
        return node

    def get_node(self, symbol: str) -> Optional[NodeConfig]:
        return self._node_configs.get(symbol)

    def estimate_fee(self, symbol: str, amount: float) -> float:
        lower, upper = self._fee_bounds[symbol]
        proportional = amount * 0.001
        return min(max(proportional, lower), upper)

    def validate_transaction(
        self, symbol: str, address: str, amount: float, fee: float
    ) -> List[str]:
        errors: List[str] = []
        account = self.get_account(symbol)
        lower, upper = self._fee_bounds[symbol]

        if amount <= 0:
            errors.append("Amount must be greater than zero.")
        if fee < lower or fee > upper:
            errors.append(
                f"Fee must be between {lower} and {upper} {symbol.lower()} for predictable costs."
            )
        if amount + fee > account.balance:
            errors.append("Insufficient balance for amount plus fee.")
        if not address:
            errors.append("Destination address is required.")
        elif symbol == "LTC" and not address.lower().startswith("l"):
            errors.append("Litecoin addresses typically start with l, L, or m.")
        elif symbol == "XMR" and address[0] not in {"4", "8"}:
            errors.append("Monero addresses usually start with 4 or 8.")

        node_configured = self.get_node(symbol)
        if not node_configured:
            errors.append("Configure a trusted node endpoint before broadcasting.")

        return errors

    def send_transaction(
        self, symbol: str, address: str, amount: float, fee: float, note: str
    ) -> str:
        if not self._profile:
            raise ValueError("Load a wallet name and seed phrase before sending.")

        account = self.get_account(symbol)
        errors = self.validate_transaction(symbol, address, amount, fee)
        if errors:
            raise ValueError("; ".join(errors))

        account.balance -= amount + fee
        tx_id = f"{symbol.lower()}-{len(account.pending) + 1:04d}"
        summary = f"{symbol} send {amount:.8f} to {address} (fee {fee:.8f})"
        if note:
            summary += f" — {note}"

        account.pending.append(summary)
        return tx_id

    def refresh_balances(self) -> None:
        for account in self._accounts.values():
            account.balance = round(account.balance, 8)
