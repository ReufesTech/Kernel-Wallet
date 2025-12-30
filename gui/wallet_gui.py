import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import scrolledtext
from datetime import datetime

from wallet_engine import WalletEngine


class WalletGUI:
    def __init__(self, root: tk.Tk, engine: WalletEngine) -> None:
        self.root = root
        self.engine = engine
        self.root.title("Kernel Wallet — Litecoin & Monero")
        self.root.geometry("900x620")
        self.root.minsize(840, 560)

        self.selected_symbol = tk.StringVar(value="LTC")
        self.wallet_name = tk.StringVar()
        self.node_endpoint = tk.StringVar()
        self.node_tls = tk.BooleanVar(value=True)
        self._node_values = {"LTC": "", "XMR": ""}
        self._last_symbol = self.selected_symbol.get()
        self.recipient = tk.StringVar()
        self.amount = tk.DoubleVar(value=0.01)
        self.fee = tk.DoubleVar()
        self.note = tk.StringVar()

        self._apply_style()
        self._build_layout()
        self._update_account_view()
        self._append_log(
            "Interface ready. Load your self-custodial wallet (name + seed phrase)"
            " and register your own node endpoints before preparing transactions."
        )

    def _apply_style(self) -> None:
        """Configure a modern, dark-forward look and feel."""

        self.root.configure(bg="#0f1624")
        style = ttk.Style()
        style.theme_use("clam")

        base_bg = "#111827"
        card_bg = "#161f31"
        accent = "#38bdf8"
        text_primary = "#e5e7eb"
        text_muted = "#9ca3af"

        style.configure("TFrame", background=base_bg)
        style.configure("TLabel", background=base_bg, foreground=text_primary, font=("Inter", 11))
        style.configure("Title.TLabel", font=("Inter", 16, "bold"), foreground=text_primary)
        style.configure("Subtitle.TLabel", font=("Inter", 11), foreground=text_muted)
        style.configure(
            "Card.TLabelframe",
            background=card_bg,
            foreground=text_primary,
            bordercolor="#1f2937",
            relief="solid",
        )
        style.configure("Card.TLabelframe.Label", background=card_bg, foreground=text_muted, font=("Inter", 10, "bold"))
        style.configure("Accent.TButton", background=accent, foreground="#0b1324", font=("Inter", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#67e8f9")])
        style.configure("TButton", padding=8, font=("Inter", 10))
        style.configure("TEntry", fieldbackground="#0b1324", foreground=text_primary, insertcolor=text_primary)
        style.configure("Badge.TLabel", background="#0ea5e9", foreground="#0b1324", padding=(8, 2), font=("Inter", 9, "bold"))
        style.configure("Danger.TLabel", background="#f43f5e", foreground="#0b1324", padding=(8, 2), font=("Inter", 9, "bold"))
        style.configure("InfoBadge.TLabel", background="#22c55e", foreground="#0b1324", padding=(8, 2), font=("Inter", 9, "bold"))
        style.configure("Warn.TLabel", background="#f59e0b", foreground="#0b1324", padding=(8, 2), font=("Inter", 9, "bold"))

    def _build_layout(self) -> None:
        outer = ttk.Frame(self.root, padding=16)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Kernel Wallet", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text=(
                "Offline-first client for Litecoin (LTC) and Monero (XMR)."
                " Validate locally, connect your own nodes, and prepare sends deliberately."
            ),
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        identity = ttk.Labelframe(outer, text="Wallet identity", style="Card.TLabelframe")
        identity.pack(fill="x", pady=(0, 8))
        identity.columnconfigure(1, weight=1)

        ttk.Label(identity, text="Wallet name").grid(row=0, column=0, sticky="w", padx=12, pady=6)
        ttk.Entry(identity, textvariable=self.wallet_name).grid(
            row=0, column=1, padx=12, pady=6, sticky="ew"
        )

        ttk.Label(identity, text="Seed phrase (kept local)").grid(
            row=1, column=0, sticky="nw", padx=12, pady=6
        )
        seed_box = tk.Text(
            identity,
            height=3,
            wrap="word",
            background="#0b1324",
            foreground="#e5e7eb",
            insertbackground="#e5e7eb",
            relief="flat",
            padx=8,
            pady=6,
        )
        seed_box.grid(row=1, column=1, padx=12, pady=6, sticky="ew")
        self.seed_box = seed_box

        identity_footer = ttk.Frame(identity)
        identity_footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=(6, 8))
        identity_footer.columnconfigure(0, weight=1)
        self.wallet_status = ttk.Label(
            identity_footer,
            text="No wallet loaded — set a name and seed to stay self-custodial.",
            style="Subtitle.TLabel",
        )
        self.wallet_status.grid(row=0, column=0, sticky="w")
        ttk.Button(
            identity_footer, text="Load wallet", style="Accent.TButton", command=self._load_wallet
        ).grid(row=0, column=1, sticky="e")

        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(0, 8))
        ttk.Label(controls, text="Asset", style="Subtitle.TLabel").pack(side="left")
        asset_menu = ttk.OptionMenu(
            controls,
            self.selected_symbol,
            self.selected_symbol.get(),
            "LTC",
            "XMR",
            command=self._switch_asset,
        )
        asset_menu.configure(width=6)
        asset_menu.pack(side="left", padx=8)
        ttk.Label(controls, text="Offline", style="Badge.TLabel").pack(side="left")
        ttk.Label(controls, text="Bring your node", style="InfoBadge.TLabel").pack(side="left", padx=(8, 0))
        ttk.Label(controls, text="Self-custody", style="Warn.TLabel").pack(side="left", padx=(8, 0))
        ttk.Button(controls, text="Refresh", command=self._refresh_balances).pack(
            side="right"
        )

        node_frame = ttk.Labelframe(outer, text="Node connectivity", style="Card.TLabelframe")
        node_frame.pack(fill="x", pady=(0, 8))
        node_frame.columnconfigure(1, weight=1)

        ttk.Label(node_frame, text="RPC endpoint (host:port)").grid(
            row=0, column=0, sticky="w", padx=12, pady=6
        )
        ttk.Entry(node_frame, textvariable=self.node_endpoint).grid(
            row=0, column=1, padx=12, pady=6, sticky="ew"
        )
        ttk.Checkbutton(node_frame, text="TLS", variable=self.node_tls).grid(
            row=0, column=2, padx=(0, 12), pady=6, sticky="e"
        )
        node_actions = ttk.Frame(node_frame)
        node_actions.grid(row=1, column=0, columnspan=3, sticky="ew", padx=12, pady=(4, 8))
        node_actions.columnconfigure(0, weight=1)
        self.node_status = ttk.Label(
            node_actions,
            text="No node configured for this asset.",
            style="Subtitle.TLabel",
        )
        self.node_status.grid(row=0, column=0, sticky="w")
        ttk.Button(node_actions, text="Save node", style="Accent.TButton", command=self._save_node).grid(
            row=0, column=1, sticky="e"
        )

        summary = ttk.Frame(outer)
        summary.pack(fill="x", pady=8)

        balance_card = ttk.Labelframe(summary, text="Balance", style="Card.TLabelframe")
        balance_card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.balance_label = ttk.Label(balance_card, text="Balance: —", font=("Inter", 18, "bold"))
        self.balance_label.pack(anchor="w", padx=12, pady=(10, 4))
        self.pending_label = ttk.Label(balance_card, text="Pending: none", style="Subtitle.TLabel")
        self.pending_label.pack(anchor="w", padx=12, pady=(0, 10))

        address_card = ttk.Labelframe(summary, text="Receiving", style="Card.TLabelframe")
        address_card.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.address_label = ttk.Label(address_card, text="Address: —", wraplength=360)
        self.address_label.pack(anchor="w", padx=12, pady=(10, 10))

        send_frame = ttk.Labelframe(outer, text="Send payment", style="Card.TLabelframe")
        send_frame.pack(fill="both", expand=True, pady=8)

        send_frame.columnconfigure(1, weight=1)
        ttk.Label(send_frame, text="Recipient address").grid(row=0, column=0, sticky="w", padx=12, pady=6)
        recipient_entry = ttk.Entry(send_frame, textvariable=self.recipient)
        recipient_entry.grid(row=0, column=1, padx=12, pady=6, sticky="ew")

        ttk.Label(send_frame, text="Amount").grid(row=1, column=0, sticky="w", padx=12, pady=6)
        amount_entry = ttk.Entry(send_frame, textvariable=self.amount, width=14)
        amount_entry.grid(row=1, column=1, padx=12, pady=6, sticky="w")

        ttk.Label(send_frame, text="Fee").grid(row=2, column=0, sticky="w", padx=12, pady=6)
        fee_row = ttk.Frame(send_frame)
        fee_row.grid(row=2, column=1, padx=12, pady=6, sticky="w")
        fee_entry = ttk.Entry(fee_row, textvariable=self.fee, width=12)
        fee_entry.pack(side="left")
        ttk.Button(
            fee_row,
            text="Estimate",
            style="Accent.TButton",
            command=self._estimate_fee,
        ).pack(side="left", padx=(8, 0))

        ttk.Label(send_frame, text="Note (local)").grid(row=3, column=0, sticky="w", padx=12, pady=6)
        ttk.Entry(send_frame, textvariable=self.note).grid(
            row=3, column=1, padx=12, pady=6, sticky="ew"
        )

        action_row = ttk.Frame(send_frame)
        action_row.grid(row=4, column=0, columnspan=2, sticky="e", padx=12, pady=(12, 8))
        ttk.Label(
            action_row,
            text="No shared infrastructure; connect your own node before broadcasting.",
            style="Subtitle.TLabel",
        ).pack(side="left", padx=(0, 12))
        ttk.Button(action_row, text="Send", style="Accent.TButton", command=self._confirm_and_send).pack(
            side="right"
        )

        log_frame = ttk.Labelframe(outer, text="Activity", style="Card.TLabelframe")
        log_frame.pack(fill="both", expand=True, pady=(8, 0))
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            wrap="word",
            state="disabled",
            background="#0b1324",
            foreground="#e5e7eb",
            insertbackground="#e5e7eb",
            relief="flat",
        )
        self.log_text.pack(fill="both", expand=True, padx=12, pady=12)

    def _update_account_view(self) -> None:
        self._node_values[self._last_symbol] = self.node_endpoint.get().strip()
        symbol = self.selected_symbol.get()
        account = self.engine.get_account(symbol)
        self.balance_label.config(text=f"{account.balance:.8f} {symbol}")
        self.address_label.config(text=f"Address: {account.address}")
        if account.pending:
            pending_text = "\n".join(account.pending)
            self.pending_label.configure(style="Danger.TLabel")
        else:
            pending_text = "None"
            self.pending_label.configure(style="Subtitle.TLabel")
        self.pending_label.config(text=f"Pending: {pending_text}")

        self.node_endpoint.set(self._node_values.get(symbol, ""))
        node = self.engine.get_node(symbol)
        if node:
            self.node_status.config(text=f"{symbol} node set to {node.display_label()}")
        else:
            self.node_status.config(text="No node configured for this asset.")
        self._last_symbol = symbol

    def _switch_asset(self, symbol: str) -> None:
        self.selected_symbol.set(symbol)
        self._update_account_view()

    def _refresh_balances(self) -> None:
        self.engine.refresh_balances()
        self._update_account_view()
        self._append_log("Balances refreshed locally.")

    def _estimate_fee(self) -> None:
        symbol = self.selected_symbol.get()
        amount = self.amount.get()
        fee = self.engine.estimate_fee(symbol, amount)
        self.fee.set(round(fee, 8))
        self._append_log(f"Estimated fee for {symbol}: {fee:.8f}")

    def _confirm_and_send(self) -> None:
        if not self.engine.has_profile():
            messagebox.showwarning(
                "Wallet not loaded",
                "Load your wallet name and seed phrase to keep keys local before sending.",
            )
            return

        symbol = self.selected_symbol.get()
        address = self.recipient.get().strip()
        amount = self.amount.get()
        fee = self.fee.get() or self.engine.estimate_fee(symbol, amount)
        note = self.note.get().strip()

        errors = self.engine.validate_transaction(symbol, address, amount, fee)
        if errors:
            messagebox.showerror("Validation failed", "\n".join(errors))
            return

        summary = (
            f"Send {amount:.8f} {symbol} to {address} with fee {fee:.8f}.\n\n"
            "Confirm to proceed. Broadcasting requires your trusted node connection."
        )
        if not messagebox.askyesno("Confirm transfer", summary):
            self._append_log("User cancelled send request.")
            return

        try:
            tx_id = self.engine.send_transaction(symbol, address, amount, fee, note)
        except ValueError as exc:
            messagebox.showerror("Cannot send", str(exc))
            return

        self._update_account_view()
        self._append_log(f"Prepared {symbol} transaction {tx_id}.")
        self._clear_form()

    def _append_log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.configure(state="disabled")
        self.log_text.see(tk.END)

    def _clear_form(self) -> None:
        self.recipient.set("")
        self.amount.set(0.01)
        self.fee.set(0.0)
        self.note.set("")

    def _load_wallet(self) -> None:
        name = self.wallet_name.get().strip()
        seed_phrase = self.seed_box.get("1.0", tk.END).strip()

        try:
            profile = self.engine.set_profile(name, seed_phrase)
        except ValueError as exc:
            messagebox.showerror("Cannot load wallet", str(exc))
            return

        self.wallet_status.config(
            text=f"Loaded wallet '{profile.name}'. Seed stays local to this session."
        )
        self._append_log("Wallet profile loaded locally for self-custody.")

    def _save_node(self) -> None:
        symbol = self.selected_symbol.get()
        endpoint = self.node_endpoint.get().strip()
        tls = self.node_tls.get()

        try:
            node = self.engine.set_node(symbol, endpoint, tls)
        except (ValueError, KeyError) as exc:
            messagebox.showerror("Cannot save node", str(exc))
            return

        self._node_values[symbol] = endpoint
        self.node_status.config(text=f"{symbol} node set to {node.display_label()}")
        self._append_log(f"Updated {symbol} node endpoint to {node.display_label()}.")


def main() -> None:
    engine = WalletEngine()
    root = tk.Tk()
    WalletGUI(root, engine)
    root.mainloop()


if __name__ == "__main__":
    main()
