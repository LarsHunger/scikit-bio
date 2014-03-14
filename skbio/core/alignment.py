#!/usr/bin/env python
r"""
Sequence collections and alignments (:mod:`skbio.core.alignment`)
================================================================

.. currentmodule:: skbio.core.alignment

This module provides functionality for working with biological sequence
collections and alignments. These can be composed of generic sequences, 
nucelotide sequences, DNA sequences, and RNA sequences.

Classes
-------

.. autosummary::
   :toctree: generated/

   SequenceCollection
   Alignment

Examples
--------
>>> from skbio.core.alignment import SequenceCollection, Alignment
>>> from skbio.core.sequence import DNA

>>> seqs = [("s1", "ACC--G-GGTA.."), ("s2", "TCC--G-GGCA..")]
>>> a1 = Alignment(seqs, DNA)

>>> from skbio.parse.fasta import MinimalFastaParser
>>> fp = "/Users/caporaso/data/gg_13_8_otus/rep_set/79_otus.fasta"
>>> s1 = SequenceCollection.from_fasta_records(MinimalFastaParser(open(fp)), DNA)
>>> s1


"""
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import numpy as np

from skbio.core.exception import SequenceCollectionError


class SequenceCollection(object):
    """
    """

    def __init__(self, seqs, validate=False):
       """
       """
       self._data = seqs
       self._identifier_to_index = dict([(seq.identifier, i) 
               for i, seq in enumerate(self._data)])
       if validate and not self.is_valid():
           raise SequenceCollectionError(
               "Something is wrong, and it's your fault.")

    @classmethod
    def from_fasta_records(cls, fasta_records, seq_constructor,
            validate=False):
        """
        """
        data = []
        for seq_id, seq in fasta_records:
            try:
                identifier, description = seq_id.split(None, 1)
            except ValueError:
                identifier = seq_id.strip()
                description = None
            data.append(seq_constructor(seq, identifier=identifier,
              description=description))
 
        return cls(data, validate=validate)

    def __eq__(self, other):
        """
        """
        if self.__class__ != other.__class__:
            return False
        elif len(self) != len(other):
            return False
        else:
            for self_seq, other_seq in zip(self,other):
                if self_seq != other_seq:
                    return False
        return True
    
    def __getitem__(self, index):
        """
        """
        if isinstance(index, str):
            return self.get_seq(index)
        else:
            return self._data[index]

    def __iter__(self):
        """
        """
        return iter(self._data)

    def degap(self):
        """
        """
        result = []
        for seq in self:
            result.append(seq.degap())
        return SequenceCollection(result)

    def int_map(self, prefix=""):
        """
        """
        int_keys = []
        int_map = []
        for i, seq in enumerate(self):
            k = ("%s%d" % (prefix, i))
            int_keys.append((k, seq.identifier))
            int_map.append((k, seq))
        return dict(int_map), dict(int_keys) 

    def get_seq(self, identifier):
        """
        """
        return self[self._identifier_to_index[identifier]]

    def identifiers(self):
        """
        """
        return self._identifier_to_index.keys()

    def items(self):
        """
        """
        for seq in self:
            yield seq.identifier, seq

    def __len__(self):
        """
        """
        return len(self._data)

    def __repr__(self):
        """The repr method.

        Returns
        -------
        str
            Returns a string representation of the object.

        Notes
        -----

        Examples
        --------

        """
        cn = self.__class__.__name__
        count, center, spread = self.count_center_spread() 
        return "<%s: n=%d; mean +/- std length=%.2f +/- %.2f>" % (cn, count,
                center, spread)

    def _validate_character_set(self):
        """
        """
        for seq in self:
            if not seq.is_valid():
                return False
        return True

    def count_center_spread(self, center_f=np.mean, spread_f=np.std):
        """
        """
        sequence_lengths = self.sequence_lengths()
        return (len(sequence_lengths), center_f(sequence_lengths),
                spread_f(sequence_lengths))

    def num_seqs(self):
        """
        """
        return len(self._data)

    def is_valid(self):
        """
        """
        return self._validate_character_set()

    def lower(self):
        """
        """
        result = []
        for seq in self:
            result.append(seq.lower())
        return self.__class__(result)

    def majority_consensis(self):
        """
        """
        raise NotImplementedError

    def sequence_lengths(self):
        """
        """
        return [len(seq) for seq in self]

    def to_fasta(self):
        """
        """
        return ''.join([seq.to_fasta() for seq in self._data])
   
    def toFasta(self):
        print "Deprecation warning!"
        return self.to_fasta()
    
    def to_phylip(self):
        """
        """
        raise NotImplementedError

    def toPhylip(self):
        """
        """
        print "Deprecation warning!"
        return self.to_phylip()

    def upper(self):
        """
        """
        result = []
        for seq in self:
            result.append(seq.upper())
        return self.__class__(result)



class Alignment(SequenceCollection):
    """
    """

    def _validate_lengths(self):
        """
        """
        seq1_length = len(self[0])
        for seq in self[1:]:
            if seq1_length != len(seq):
                return False
        return True

    def alignment_length(self):
        return len(self._data[0])

    def distances(self):
        """
        """
        raise NotImplementedError

    def get_subalignment(self, seqs_to_keep=None, positions_to_keep=None,
            invert_seqs_to_keep=False, invert_positions_to_keep=False):
        """
        """
        raise NotImplementedError

    def is_valid(self):
        """
        """
        return super(Alignment, self).is_valid() and self._validate_lengths()

    def iter_positions(self):
        """
        """
        raise NotImplementedError

    def majority_consensus(self):
        """
        """
        raise NotImplementedError


    def omit_gap_sequences(self, allowed_gap_frac=0):
        """
        """
        raise NotImplementedError

    def omit_gap_positions(self, allowed_gap_frac=0):
        """
        """
        raise NotImplementedError

    def positional_frequencies(self):
        """
        """
        raise NotImplementedError

    def uncertainties(self):
        """
        """
        raise NotImplementedError
