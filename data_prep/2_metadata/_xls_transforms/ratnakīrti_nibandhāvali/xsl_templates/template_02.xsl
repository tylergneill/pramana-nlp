<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="gap|sic|" />

<xsl:template match="//pb[not(@ed='thakur75' or @edRef='#thakur75' or @xml:id='thakur75-130')]" />
<xsl:template match="//lb[not(@ed='thakur75')]" />

<xsl:template match="//pb[@ed='thakur75' or @edRef='#thakur75' or @xml:id='thakur75-130']">
<xsl:text>〈</xsl:text><xsl:value-of select="@xml:id"/><xsl:text>〉</xsl:text>
</xsl:template>

<xsl:template match="//lb[@ed='thakur75']">
<xsl:text>〈</xsl:text><xsl:value-of select="@xml:id"/><xsl:text>〉</xsl:text>
</xsl:template>

<xsl:template match="bibl|span|corr|hi|note/note">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="anchor[not(substring(@xml:id,1,3)='tha')]" />

<xsl:template match="pb[not(substring(@xml:id,1,3)='tha')]" />

</xsl:stylesheet>