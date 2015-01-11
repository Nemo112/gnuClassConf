#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file UError.py
# \brief Třída, která slouží k posílání chyb


class UError:

    """
    \brief Třída obsahující funkce pro posílání chyb pomocí
    raise
    """

    def __init__(self, arg):
        """
        Konstruktor
        \param arg String obsahující popis chyby
        \param self Ukazatel na objekt
        """
        # argument závady
        self.args = arg
