<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="teiHeader" />

<xsl:template match="front" />

<xsl:template match="comment()"/>

<xsl:template match="ref" />

<xsl:template match="note[@type='correction']">
<xsl:text>(</xsl:text>
<xsl:value-of select="."/>
<xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="note[@type='corrected']" />
<xsl:template match="note[@type='noreference']" />
<xsl:template match="note[not(@type)]" />

<xsl:template match="hi">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="lb[@break='no']" />

<xsl:template match="pb[@ed='ms']"/>

</xsl:stylesheet>
